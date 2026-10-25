"""Extra tests added by the candidate. The original test_profitability.py is unchanged."""

import json
import math
import random
import unittest
from decimal import Decimal

from profitability import calculate_load

# Same load as test_normal_load, as keyword arguments so each test can change one field.
BASE = dict(revenue=2000, miles=500, fuel_price=4, mpg=10, driver_pay=400, tolls=50,
            dispatch_pct=10, other_expenses=100, desired_margin_pct=20)


def calc(**changes):
    return calculate_load(**{**BASE, **changes})


class FormulaTests(unittest.TestCase):
    """One test per contract formula, with numbers that tell the right formula from the planted one."""

    def test_fuel_divides_miles_by_mpg(self):
        # 600 miles at 8 mpg = 75 gallons x $4.20 = $315 (miles x mpg x price would be $20,160).
        self.assertEqual(calc(miles=600, mpg=8, fuel_price=4.2)["fuel_cost"], 315.00)

    def test_dispatch_pct_is_on_a_0_to_100_scale(self):
        # 8% of $2,500 is $200 (not 2,500 x 8 = $20,000).
        self.assertEqual(calc(revenue=2500, dispatch_pct=8)["dispatch_fee"], 200.00)

    def test_margin_is_profit_over_revenue_not_cost(self):
        r = calc()
        self.assertEqual(r["margin_pct"], 52.50)  # 1050 / 2000; profit / cost would be 110.53

    def test_loss_making_load_has_negative_profit_and_margin(self):
        r = calc(revenue=800)  # cost = 200 + 400 + 50 + 80 + 100 = 830
        self.assertEqual(r["total_cost"], 830.00)
        self.assertEqual(r["profit"], -30.00)
        self.assertEqual(r["margin_pct"], -3.75)

    def test_break_even_covers_dispatch_fee(self):
        # Fixed costs 750 at 10% dispatch: 750 / 0.9 = 833.33. Without the gross-up it would be 750.
        self.assertEqual(calc()["break_even_rate"], 833.33)

    def test_suggested_rate_hits_net_margin_after_dispatch(self):
        # 750 / (1 - 0.10 - 0.20) = 1071.43. The old formula gave 833.33 / 0.8 = 1041.67.
        self.assertEqual(calc()["suggested_rate"], 1071.43)

    def test_no_dispatch_no_margin_means_break_even_equals_fixed_costs(self):
        r = calc(dispatch_pct=0, desired_margin_pct=0)
        self.assertEqual(r["break_even_rate"], 750.00)
        self.assertEqual(r["suggested_rate"], 750.00)
        self.assertEqual(r["dispatch_fee"], 0.00)

    def test_result_has_exactly_the_contract_fields(self):
        self.assertEqual(set(calc()), {"fuel_cost", "dispatch_fee", "total_cost", "profit",
                                       "margin_pct", "break_even_rate", "suggested_rate"})


class RoundTripTests(unittest.TestCase):
    """Feed the calculator's own rates back in: the break-even rate should make about $0,
    and the suggested rate should hit the target margin. Checked on 500 seeded random loads."""

    def setUp(self):
        self.rng = random.Random(2026)

    def random_load(self):
        dispatch = self.rng.choice([0, 5, 8, 10, 12.5, 15])
        return dict(
            revenue=round(self.rng.uniform(0, 6000), 2), miles=round(self.rng.uniform(0, 2500), 1),
            fuel_price=round(self.rng.uniform(3, 6), 3), mpg=round(self.rng.uniform(4, 9), 1),
            driver_pay=round(self.rng.uniform(0, 1500), 2), tolls=round(self.rng.uniform(0, 200), 2),
            dispatch_pct=dispatch, other_expenses=round(self.rng.uniform(0, 400), 2),
            desired_margin_pct=self.rng.choice([0, 10, 15, 20, 25, 30]),
        )

    def test_break_even_rate_gives_zero_profit(self):
        for _ in range(500):
            load = self.random_load()
            rate = calculate_load(**load)["break_even_rate"]
            with self.subTest(load=load):
                profit = calculate_load(**{**load, "revenue": rate})["profit"]
                self.assertLessEqual(abs(profit), 0.01)

    def test_suggested_rate_meets_target_margin(self):
        for _ in range(500):
            load = self.random_load()
            r = calculate_load(**load)
            if r["suggested_rate"] == 0:
                continue  # no costs at all: any margin target is met at $0
            with self.subTest(load=load):
                margin = calculate_load(**{**load, "revenue": r["suggested_rate"]})["margin_pct"]
                self.assertLessEqual(abs(margin - load["desired_margin_pct"]), 0.01)

    def test_displayed_fields_always_add_up(self):
        for _ in range(500):
            load = self.random_load()
            r = calculate_load(**load)
            with self.subTest(load=load):
                parts = (Decimal(str(r["fuel_cost"])) + Decimal(str(load["driver_pay"]))
                         + Decimal(str(load["tolls"])) + Decimal(str(r["dispatch_fee"]))
                         + Decimal(str(load["other_expenses"])))
                self.assertEqual(Decimal(str(r["total_cost"])), parts)
                self.assertEqual(Decimal(str(r["profit"])),
                                 Decimal(str(load["revenue"])) - Decimal(str(r["total_cost"])))


class ZeroRevenueTests(unittest.TestCase):
    def test_zero_revenue_with_costs_uses_minus_100_sentinel(self):
        r = calc(revenue=0)
        self.assertLess(r["profit"], 0)
        self.assertEqual(r["margin_pct"], -100.00)

    def test_zero_revenue_and_zero_cost_is_zero_margin_not_a_crash(self):
        # The original code divided by total cost and raised ZeroDivisionError here.
        r = calculate_load(0, 0, 0, 10, 0, 0, 10, 0, 20)
        self.assertEqual(r["profit"], 0.00)
        self.assertEqual(r["margin_pct"], 0.00)
        self.assertEqual(r["break_even_rate"], 0.00)


class RoundingTests(unittest.TestCase):
    def test_half_cent_rounds_up(self):
        # 10% of $1.25 is $0.125. round(0.125, 2) on a float gives 0.12; money rounding gives 0.13.
        self.assertEqual(calc(revenue=1.25)["dispatch_fee"], 0.13)

    def test_float_inputs_do_not_leak_binary_error(self):
        # 0.1 + 0.2 is 0.30000000000000004 in float math.
        r = calc(driver_pay=0.1, tolls=0.2, miles=0, other_expenses=0, revenue=0, dispatch_pct=0)
        self.assertEqual(r["total_cost"], 0.30)

    def test_every_field_has_at_most_two_decimals(self):
        r = calc(miles=333, mpg=7, fuel_price=3.999)
        for name, value in r.items():
            with self.subTest(field=name):
                self.assertEqual(value, round(value, 2))


class ValidationTests(unittest.TestCase):
    def assertRejected(self, **changes):
        with self.assertRaises(ValueError):
            calc(**changes)

    def test_each_money_field_and_miles_must_be_nonnegative(self):
        for field in ("revenue", "miles", "fuel_price", "driver_pay", "tolls", "other_expenses"):
            with self.subTest(field=field):
                self.assertRejected(**{field: -0.01})

    def test_mpg_must_be_above_zero(self):
        self.assertRejected(mpg=0)
        self.assertRejected(mpg=-5)

    def test_percentages_must_be_0_to_below_100(self):
        for field in ("dispatch_pct", "desired_margin_pct"):
            with self.subTest(field=field):
                self.assertRejected(**{field: -1, ("desired_margin_pct" if field == "dispatch_pct" else "dispatch_pct"): 0})
                self.assertRejected(**{field: 100, ("desired_margin_pct" if field == "dispatch_pct" else "dispatch_pct"): 0})

    def test_dispatch_plus_margin_must_be_below_100(self):
        self.assertRejected(dispatch_pct=50, desired_margin_pct=50)
        self.assertRejected(dispatch_pct=60, desired_margin_pct=45)
        # Just under the limit is allowed.
        self.assertGreater(calc(dispatch_pct=49.99, desired_margin_pct=50)["suggested_rate"], 0)

    def test_nan_and_infinity_are_rejected(self):
        for bad in (math.nan, math.inf, -math.inf, Decimal("NaN"), Decimal("Infinity")):
            for field in ("revenue", "mpg", "dispatch_pct", "driver_pay"):
                with self.subTest(field=field, value=bad):
                    self.assertRejected(**{field: bad})

    def test_non_numbers_are_rejected_with_value_error(self):
        # A JSON API can send strings, null or booleans. These must be ValueError, not TypeError.
        for bad in ("2000", None, True, False, [2000], {"amount": 2000}):
            with self.subTest(value=bad):
                self.assertRejected(revenue=bad)

    def test_zero_values_that_are_allowed(self):
        r = calc(miles=0, fuel_price=0, driver_pay=0, tolls=0, other_expenses=0,
                 dispatch_pct=0, desired_margin_pct=0)
        self.assertEqual(r["total_cost"], 0.00)
        self.assertEqual(r["margin_pct"], 100.00)


class JsonApiTests(unittest.TestCase):
    def test_accepts_a_parsed_json_body_and_returns_serializable_numbers(self):
        body = json.loads('{"revenue": 2000, "miles": 500, "fuel_price": 4.0, "mpg": 10, "driver_pay": 400,'
                          ' "tolls": 50, "dispatch_pct": 10, "other_expenses": 100, "desired_margin_pct": 20}')
        out = json.loads(json.dumps(calculate_load(**body)))
        self.assertEqual(out["suggested_rate"], 1071.43)
        self.assertTrue(all(isinstance(v, float) and math.isfinite(v) for v in out.values()))


if __name__ == "__main__":
    unittest.main()
