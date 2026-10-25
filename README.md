# FDL Final Debugging Challenge — Candidate Copy

This is a deliberately defective **fictional** calculation module. Fix defects without changing the business contract below. Do not alter the expected values in the tests to make them pass. You may add tests.

## Run
`python -m unittest -v` (Python 3.10+; no third-party packages).

## Business contract
- `dispatch_pct` and `desired_margin_pct` are percentages on a 0–100 scale (e.g. 10 means 10%).
- Fuel expense = miles / mpg × fuel price.
- Dispatch fee = revenue × dispatch_pct / 100.
- Total cost includes fuel, driver pay, tolls, dispatch fee, and other expenses.
- Profit = revenue − total cost. Profit margin = profit / revenue × 100; when revenue is zero and profit is negative, use -100 as the defined sentinel for this exercise (document this convention).
- Break-even rate must cover fixed costs and the dispatch fee percentage.
- Suggested rate must meet the desired **net profit margin on revenue**, after the dispatch fee.
- Nonnegative finite monetary inputs and miles are required; mpg > 0; 0 ≤ dispatch_pct < 100; 0 ≤ desired_margin_pct < 100; sum of dispatch percentage and target margin must be < 100. Reject invalid inputs with ValueError.
- Round displayed result fields to two decimal places.

## Deliverables
1. Corrected source and passing automated tests.
2. Bug report identifying each defect, impact, root cause, and fix.
3. Evidence of tests before/after, plus additional edge-case tests.
4. Brief note on how you verified the fix and used AI tools, if any.

Do not edit the original FDL application. Do not access real accounts. Both finalists receive the same files.
