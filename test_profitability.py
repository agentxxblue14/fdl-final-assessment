import unittest
from profitability import calculate_load

class ProfitabilityTests(unittest.TestCase):
    def test_normal_load(self):
        r=calculate_load(2000,500,4,10,400,50,10,100,20)
        self.assertAlmostEqual(r["fuel_cost"],200)
        self.assertAlmostEqual(r["dispatch_fee"],200)
        self.assertAlmostEqual(r["total_cost"],950)
        self.assertAlmostEqual(r["profit"],1050)
        self.assertAlmostEqual(r["margin_pct"],52.5)
        self.assertAlmostEqual(r["break_even_rate"],833.33,places=2)
        self.assertAlmostEqual(r["suggested_rate"],1071.43,places=2)
    def test_zero_mpg_rejected(self):
        with self.assertRaises(ValueError):calculate_load(1000,100,4,0,100,0,10,0,20)
    def test_negative_expense_rejected(self):
        with self.assertRaises(ValueError):calculate_load(1000,100,4,10,-100,0,10,0,20)
    def test_invalid_margin_rejected(self):
        with self.assertRaises(ValueError):calculate_load(1000,100,4,10,100,0,10,0,100)
    def test_zero_revenue_margin(self):
        r=calculate_load(0,100,4,10,100,0,10,0,20)
        self.assertEqual(r["margin_pct"],0 if r["profit"]==0 else -100)

if __name__=='__main__':unittest.main()
