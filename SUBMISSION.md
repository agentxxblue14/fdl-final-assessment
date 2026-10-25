# Candidate Submission

Judah Rivera, FDL Lead Developer final assessment, 26 October 2026.

**Hours spent:** HOURS_TBD (debugging challenge and development plan together)
**AI tools used:** Claude Code (Anthropic). Details in "How I verified the fix and used AI" below.

## In plain words

The calculator had **6 bugs**. It overstated fuel 100 times, charged a 10% dispatch fee as 1000%, measured margin against cost instead of revenue, set a break-even rate that would lose money, suggested a rate that missed the target margin, and accepted bad input such as 0 mpg or negative costs. All 6 are fixed. I also changed how cents are rounded so the displayed numbers always add up, and I explain that change separately because the contract does not require it.

Before: 5 tests, 1 passing (by accident). After: **32 tests, all passing**, on Python 3.10 to 3.13. Your expected values were not changed.

This repo has two parts:

1. **The corrected calculator**: `profitability.py`, your original tests (unchanged), 27 new tests in `test_edge_cases.py`, and the test output in `evidence/`.
2. **The plan, timeline and cost estimate for the whole platform**: [`PLAN.md`](PLAN.md), with the estimate model in [`plan/estimate_model.py`](plan/estimate_model.py).

The git history shows the work in order: the first commit is your files exactly as received, the next commits are the fix, the tests and the plan.

## Defects

"Observed" shows what the original code returned for the README's example load (revenue $2,000, 500 miles, $4 fuel, 10 mpg, $400 driver pay, $50 tolls, 10% dispatch, $100 other, 20% target margin).

| ID | Observed failure | Root cause | Fix | Verification |
|---|---|---|---|---|
| D1 | Fuel cost **$20,000 instead of $200**. | `miles * mpg * fuel_price` multiplies by miles per gallon. Gallons used is miles **divided** by mpg. | `miles / mpg * fuel_price` | `test_normal_load`, `test_fuel_divides_miles_by_mpg` (600 mi at 8 mpg x $4.20 = $315) |
| D2 | Dispatch fee **$20,000 instead of $200**. | `revenue * dispatch_pct` treats 10 as 1000%. The contract says percentages are on a 0 to 100 scale. | `revenue * dispatch_pct / 100` | `test_normal_load`, `test_dispatch_pct_is_on_a_0_to_100_scale` |
| D3 | Margin was profit divided by **cost**: once D1 and D2 are fixed it would show 110.53% instead of 52.5%. A load with no revenue and no costs crashed (division by zero). | Wrong denominator, and no rule for zero revenue. | Margin = profit / revenue x 100. Zero revenue: -100 when profit is negative (the contract's sentinel), 0 when profit is also zero. | `test_normal_load`, `test_margin_is_profit_over_revenue_not_cost`, `test_zero_revenue_and_zero_cost_is_zero_margin_not_a_crash`, `test_zero_revenue_with_costs_uses_minus_100_sentinel` |
| D4 | Break-even rate **$20,550** on the original code (inflated by D1). With D1 and D2 fixed, the same formula gives **$750 instead of $833.33**: a dispatcher who accepted the load at "break-even" would lose the $75 dispatch fee. | It added the fixed costs but ignored that the dispatch fee is a share of the rate itself. | Fixed costs / (1 - dispatch share). This solves: rate - fixed costs - rate x dispatch % = 0. | `test_normal_load`, `test_break_even_covers_dispatch_fee`, plus 500 random loads: charging the break-even rate gives a profit within 1 cent of $0 |
| D5 | Suggested rate **$25,687.50** on the original code. With D1 and D2 fixed, the same formula gives **$1,041.67 instead of $1,071.43**, and at $1,041.67 the real margin after the dispatch fee is 18%, not the 20% asked for. | It divided the break-even rate by (1 - margin), which stacks the two percentages instead of taking both from revenue. | Fixed costs / (1 - dispatch share - margin share). This solves: rate - fixed costs - rate x dispatch % = rate x margin %. | `test_normal_load`, `test_suggested_rate_hits_net_margin_after_dispatch`, plus 500 random loads: charging the suggested rate gives the target margin within 0.01 points |
| D6 | Bad input accepted or crashed with the wrong error. Accepted: mpg of 0, negative driver pay, tolls and other expenses, dispatch + margin of 100% or more, "not a number" and infinity, `true`/`false` (treated as 1 and 0). Wrong error: a 100% margin crashed with a division error, and text or null from a JSON API crashed with a type error, instead of ValueError. | Only 4 of the 9 inputs were checked, the mpg check was `< 0` instead of `<= 0`, and types, finiteness and the percentage rules were not checked. | Every input must be a finite number (not text, null or true/false). Money and miles 0 or more, mpg above 0, each percentage at least 0 and below 100, their sum below 100. Every failure raises ValueError naming the field. Values too large to calculate to the cent are rejected the same way. | `test_zero_mpg_rejected`, `test_negative_expense_rejected`, `test_invalid_margin_rejected`, and 10 validation tests in `test_edge_cases.py` |

One more finding about the original tests: **`test_zero_revenue_margin` passed on the broken code by accident.** With zero revenue, profit equals minus total cost, so profit / total cost happened to be -100 too. The new zero-revenue, zero-cost test exposes the real problem.

### A rounding change I made, and why (H1)

This is not a contract violation, so I list it apart from the defects. The contract only says "round to two decimal places".

| | |
|---|---|
| Problem | With D1 to D6 fixed but ordinary computer decimals (floats) and Python's `round()`: 10% of $1.25 = $0.125 is shown as **$0.12**, and in **116 of 500 random loads** the displayed total cost did not equal the sum of the displayed cost lines, or the displayed profit did not equal revenue minus the displayed total. An owner checking the numbers by hand would find they don't add up. |
| Change | Exact decimal math, half-up rounding to the cent (the usual invoice rule), cost lines rounded first and totals built from the rounded lines, so the displayed numbers always add up. Results are still returned as ordinary numbers, so the API looks the same. |
| Evidence | `test_half_cent_rounds_up`, `test_displayed_fields_always_add_up` (500 loads), `evidence/float-only-fix-comparison.txt` (a float-only fix fails 121 checks of the same suite). |

### Conventions I documented (the contract asked for this)

- **Zero revenue:** margin is -100.00 when profit is negative and 0.00 when profit is also zero. Profit cannot be positive with zero revenue because every cost must be 0 or more.
- **Rounding:** half-up to two decimals; cost lines first, totals are sums of the rounded lines. -0.00 is shown as 0.00.
- **Break-even and suggested rate** are rounded to the nearest cent like the other fields (your test expects 833.33, not 833.34). In the product I would show the break-even rate rounded **up** to the next cent so it never falls a fraction of a cent short. That needs your agreement because it changes an expected value.

## Test execution

Before the fix (original code):

```
> python -m unittest -v
test_invalid_margin_rejected ... ERROR      (ZeroDivisionError: float division by zero)
test_negative_expense_rejected ... FAIL     (ValueError not raised)
test_normal_load ... FAIL                   (AssertionError: 20000 != 200 within 7 places)
test_zero_mpg_rejected ... FAIL             (ValueError not raised)
test_zero_revenue_margin ... ok             (passes by accident, see above)

Ran 5 tests
FAILED (failures=3, errors=1)
```

Full output: [`evidence/tests-before.txt`](evidence/tests-before.txt)

After the fix:

```
> python -m unittest -v
Ran 32 tests
OK
```

Full output with every test name: [`evidence/tests-after.txt`](evidence/tests-after.txt). GitHub Actions runs the same command on Python 3.10, 3.11, 3.12 and 3.13 on every push.

The new tests catch the planted bugs. Run against the **original** code, 23 of the 27 new tests fail: [`evidence/edge-tests-against-original-code.txt`](evidence/edge-tests-against-original-code.txt). The 4 that still pass are guards for later changes (field names, two-decimal output, a float sum case that `round()` happens to hide, and the zero-revenue case that passed by accident).

Your expected values were not changed: `git diff af3c023 -- test_profitability.py` is empty.

## Edge cases and remaining limitations

Covered by tests: zero revenue with and without costs, a loss-making load, no dispatch fee and no margin, half-cent rounding, float inputs such as 0.1 + 0.2, every money field negative, -0, mpg 0 and negative, percentages at -1 and 100, dispatch + margin at 100 and above and just under, "not a number" and infinity, text, null, true/false, lists and objects, absurdly large values, a $1 billion load, a parsed JSON body in and JSON out, and 500 random loads for the break-even, suggested-rate and add-up checks.

Remaining limitations, by design of the exercise:

- One currency (USD), no currency field.
- No business upper limits (for example a maximum miles per load), so a typo such as 50,000 miles is accepted. A real API should add sensible limits agreed with the owner. Only values too large to calculate to the cent are rejected.
- The dispatch fee is a percentage of total revenue, as this contract says. The Master Sheet says the Full Dispatch fee is 10% of **linehaul revenue only**. If a load has fuel surcharge or accessorial charges, these differ. This is question 2 in PLAN.md.
- Text such as "2000" is rejected rather than converted. A form-based client should send numbers.
- The calculator uses a single flat cost list. The product version in the Master Sheet (section A) uses cost profiles, cost per mile with loaded and deadhead miles, and saved estimates. PLAN.md workstream 9 covers that.

## How I verified the fix and used AI

**Tool:** Claude Code (Anthropic), working in this repo on my machine. Only the supplied files and fictional data were used.

**What the AI did:** read the README contract and the code, found the defects, wrote the corrected `profitability.py`, the new tests, this report, and the first draft of the plan and its estimate model. A separate AI session that had not written any of it then reviewed the whole submission as a skeptical CTO; its findings were fixed (the timeline model now plans the Lead's and the TA's hours separately, five month labels were corrected, the cost estimate was raised, and two input edge cases were closed).

**How the output was checked, not just trusted:**

1. Your files were committed unchanged first and your tests were run on them, so the "before" results are real output.
2. Each formula was checked by hand on the README load: fuel 500 / 10 x 4 = 200, dispatch 2,000 x 10 / 100 = 200, total 950, profit 1,050, margin 52.5%, break-even 750 / 0.9 = 833.33, suggested 750 / 0.7 = 1,071.43.
3. The new tests were run against the **original** code to prove they catch the bugs (23 of 27 fail there). A test that passes on broken code proves nothing.
4. A float-only version of the fix was run against the same tests, to check the rounding change fixes a real problem and is not just style.
5. Round-trip checks feed the calculator's own break-even and suggested rates back in and confirm they produce $0 profit and the target margin on 500 random loads.
6. The plan's hours, dates and cost totals come from a script, so they cannot drift apart when one assumption changes.

## GitHub / Replit links

- GitHub: GITHUB_URL
- Replit: not used for this part. The challenge says to work only on the supplied files, and it runs with plain Python (`python -m unittest -v`), no packages needed.
