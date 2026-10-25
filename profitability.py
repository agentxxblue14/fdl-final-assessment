"""FDL fictional load profitability service. Diagnose and fix defects.
No external dependencies. Monetary inputs are USD.
"""

def calculate_load(revenue, miles, fuel_price, mpg, driver_pay, tolls, dispatch_pct, other_expenses, desired_margin_pct):
    # Input values may arrive as numbers from a JSON API.
    if revenue < 0 or miles < 0 or fuel_price < 0 or mpg < 0:
        raise ValueError("Invalid input")
    fuel_cost = miles * mpg * fuel_price
    dispatch_fee = revenue * dispatch_pct
    total_cost = fuel_cost + driver_pay + tolls + dispatch_fee + other_expenses
    profit = revenue - total_cost
    margin_pct = (profit / total_cost) * 100
    break_even_rate = fuel_cost + driver_pay + tolls + other_expenses
    suggested_rate = break_even_rate / (1 - desired_margin_pct / 100)
    return {
        "fuel_cost": round(fuel_cost, 2),
        "dispatch_fee": round(dispatch_fee, 2),
        "total_cost": round(total_cost, 2),
        "profit": round(profit, 2),
        "margin_pct": round(margin_pct, 2),
        "break_even_rate": round(break_even_rate, 2),
        "suggested_rate": round(suggested_rate, 2),
    }
