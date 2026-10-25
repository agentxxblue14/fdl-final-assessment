"""FDL fictional load profitability service.
No external dependencies. Monetary inputs are USD.

Conventions (documented as the business contract asks):
- Math is done in Decimal, not float, so cents are exact. Inputs are
  converted through str(), so 0.1 becomes Decimal("0.1"), not the binary
  approximation of 0.1.
- Money line items (fuel cost, dispatch fee) are rounded to the cent first,
  and totals are built from those rounded lines, so the displayed fields
  always add up: total_cost = fuel + driver pay + tolls + dispatch + other,
  and profit = revenue - total_cost, to the cent.
- Rounding is half-up to two decimal places (0.125 -> 0.13), the usual rule
  on invoices. Python's round() on a float can give 0.12 for the same value.
- Zero revenue: margin_pct is -100.00 when profit is negative (the sentinel
  the contract defines) and 0.00 when profit is also zero (nothing earned,
  nothing spent). Profit cannot be positive when revenue is zero because
  every cost input must be nonnegative.
- Results are returned as floats rounded to two places, the same shape as
  before, so a JSON API can serialize them unchanged.
"""

import math
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext

CENT = Decimal("0.01")
HUNDRED = Decimal(100)

_MONEY_AND_MILES = ("revenue", "miles", "fuel_price", "driver_pay", "tolls", "other_expenses")


def _to_decimal(name, value):
    # Input values may arrive as numbers from a JSON API. bool is a subclass of
    # int in Python, so a JSON true/false would otherwise pass as 1 or 0.
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError(f"{name} must be a number, got {type(value).__name__}")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if isinstance(value, Decimal) and not value.is_finite():
        raise ValueError(f"{name} must be finite")
    number = Decimal(str(value))
    return number if number != 0 else Decimal(0)  # -0.0 would otherwise show as -0.0


def _money(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def calculate_load(revenue, miles, fuel_price, mpg, driver_pay, tolls, dispatch_pct, other_expenses, desired_margin_pct):
    args = {
        "revenue": revenue, "miles": miles, "fuel_price": fuel_price, "mpg": mpg,
        "driver_pay": driver_pay, "tolls": tolls, "dispatch_pct": dispatch_pct,
        "other_expenses": other_expenses, "desired_margin_pct": desired_margin_pct,
    }
    d = {name: _to_decimal(name, value) for name, value in args.items()}

    for name in _MONEY_AND_MILES:
        if d[name] < 0:
            raise ValueError(f"{name} must be zero or more")
    if d["mpg"] <= 0:
        raise ValueError("mpg must be greater than zero")
    if not 0 <= d["dispatch_pct"] < 100:
        raise ValueError("dispatch_pct must be at least 0 and below 100")
    if not 0 <= d["desired_margin_pct"] < 100:
        raise ValueError("desired_margin_pct must be at least 0 and below 100")
    if d["dispatch_pct"] + d["desired_margin_pct"] >= 100:
        raise ValueError("dispatch_pct plus desired_margin_pct must be below 100")

    # 50 significant digits is far more than any real load needs; a value too large to
    # compute to the cent is rejected instead of crashing with decimal.InvalidOperation.
    try:
        with localcontext() as ctx:
            ctx.prec = 50
            fuel_cost = _money(d["miles"] / d["mpg"] * d["fuel_price"])
            dispatch_fee = _money(d["revenue"] * d["dispatch_pct"] / HUNDRED)
            fixed_costs = fuel_cost + d["driver_pay"] + d["tolls"] + d["other_expenses"]
            total_cost = _money(fixed_costs + dispatch_fee)
            profit = _money(d["revenue"] - total_cost)

            if d["revenue"] > 0:
                margin_pct = profit / d["revenue"] * HUNDRED
            else:
                margin_pct = Decimal(-100) if profit < 0 else Decimal(0)

            # The dispatch fee is a share of the rate itself, so the rate has to be
            # grossed up: rate - fixed - rate * dispatch = 0.
            dispatch_share = d["dispatch_pct"] / HUNDRED
            break_even_rate = fixed_costs / (1 - dispatch_share)
            # Net margin on revenue after the dispatch fee:
            # rate - fixed - rate * dispatch = rate * margin.
            margin_share = d["desired_margin_pct"] / HUNDRED
            suggested_rate = fixed_costs / (1 - dispatch_share - margin_share)

            margin_pct, break_even_rate, suggested_rate = (
                _money(margin_pct), _money(break_even_rate), _money(suggested_rate))
    except InvalidOperation:
        raise ValueError("inputs are too large to calculate to the cent") from None

    return {
        "fuel_cost": float(fuel_cost),
        "dispatch_fee": float(dispatch_fee),
        "total_cost": float(total_cost),
        "profit": float(profit),
        "margin_pct": float(margin_pct),
        "break_even_rate": float(break_even_rate),
        "suggested_rate": float(suggested_rate),
    }
