# reason-1: Discount and tax word problem (reasoning)

## Hidden rubric (never shown to the model under test)

Expected answer: Sarah receives $18.12 in change.

Worked arithmetic (the judge should verify the model's steps against this):
- Pens: 7 x $2.25 = $15.75
- Notebooks before discount: 3 x $5.40 = $16.20
- Coupon (15% of notebooks only): $16.20 x 0.15 = $2.43
- Notebooks after discount: $16.20 - $2.43 = $13.77
- Subtotal after discount: $15.75 + $13.77 = $29.52
- Sales tax (8% of the discounted subtotal): $29.52 x 0.08 = $2.3616, rounds to $2.36
- Total: $29.52 + $2.36 = $31.88 (computing $29.52 x 1.08 = $31.8816 directly also
  rounds to $31.88, so rounding order does not change the answer)
- Change from $50: $50.00 - $31.88 = $18.12

Common wrong answers and what they indicate:
- $20.67: applied the 15% coupon to the whole purchase, not just notebooks.
- $20.48: forgot to apply sales tax.
- $17.92: applied the 8% tax to the pre-discount subtotal, then subtracted the
  discount (tax before discount).
- $15.49: forgot the notebook discount entirely.
- $18.04: applied the coupon to the pens instead of the notebooks.

Score signals (each 0-2, judge totals to 10 then normalises):
- ANSWER: final change is exactly $18.12 (2), off by rounding only, i.e. $18.11 or
  $18.13 (1), anything else (0).
- STEPS: each intermediate value above appears and is correct (2 = all, 1 = one slip
  that is carried consistently, 0 = steps missing or wrong).
- SCOPE: discount applied to notebooks only, tax applied after the discount to the
  whole subtotal (2 = both right, 1 = one right, 0 = neither).
- CLARITY: a reader can follow the calculation without redoing it; final answer is
  clearly marked and stated in dollars and cents.
- CONCISION: no padding, no restating the problem at length, no alternative answers
  offered "just in case".

Objective checks: the response contains "18.12"; the last line that contains a dollar
amount contains "18.12" and no other dollar amount; the response does not give
"20.67", "20.48", "17.92", "15.49" or "18.04" as a final answer.

## Shared material (appears verbatim in every variant where the prompt refers to it)

<problem>
A stationery store sells pens for $2.25 each and notebooks for $5.40 each. Sarah buys
7 pens and 3 notebooks. She has a coupon for 15% off that applies only to the
notebooks. Sales tax of 8% is added to the whole purchase after the discount. She pays
with a $50 bill. How much change does she receive?
</problem>

## Variants

### P0 bare
Can you work this out for me?

<problem>...</problem>

### P1 specific
Solve the word problem below and give the exact amount of change Sarah receives, in
dollars and cents.

<problem>...</problem>

### P2 role
You are a careful bookkeeper who checks every line of a receipt. Solve the word problem
below and give the exact amount of change Sarah receives, in dollars and cents.

<problem>...</problem>

### P3 context
Solve the word problem below and give the exact amount of change Sarah receives, in
dollars and cents.

Background you should use: this store applies coupons before tax, and tax is charged on
the discounted subtotal of the whole basket. Amounts are rounded to the nearest cent at
the point where tax is calculated. The coupon is item-specific and does not touch the
pens.

<problem>...</problem>

### P4 constraints
Solve the word problem below and give the exact amount of change Sarah receives, in
dollars and cents.

Constraints: do not estimate or round until the tax step, and then round to the nearest
cent. Do not apply the coupon to the pens. Do not apply tax before the discount. Give
exactly one final answer; do not offer alternatives. Show every intermediate amount.

<problem>...</problem>

### P5 format
Solve the word problem below and give the exact amount of change Sarah receives, in
dollars and cents.

Output format: one labelled line per step, in this order, each with a dollar amount:
Pens:
Notebooks before discount:
Discount:
Notebooks after discount:
Subtotal:
Tax:
Total:
Change:
Then a final line exactly of the form "Answer: $X.XX". No other text.

<problem>...</problem>

### P6 fewshot
Solve the word problem below and give the exact amount of change Sarah receives, in
dollars and cents.

Here are two worked examples in the style we want:

<example>
Problem: Mugs are $3.50 each and plates are $6.00 each. Tom buys 4 mugs and 2 plates.
He has a 10% coupon that applies only to plates. Tax of 5% is added after the
discount. He pays with $40. What is his change?
Solution: Mugs 4 x 3.50 = 14.00. Plates 2 x 6.00 = 12.00; 10% off = 1.20; plates after
discount 10.80. Subtotal 14.00 + 10.80 = 24.80. Tax 5% of 24.80 = 1.24. Total 26.04.
Change 40.00 - 26.04 = 13.96.
Answer: $13.96
</example>

<example>
Problem: Shirts are $12.00 each. Priya buys 3 shirts with a 20% coupon that applies to
shirts. Tax of 6% is added after the discount. She pays with $40. What is her change?
Solution: Shirts 3 x 12.00 = 36.00; 20% off = 7.20; after discount 28.80. Tax 6% of
28.80 = 1.728, rounds to 1.73. Total 30.53. Change 40.00 - 30.53 = 9.47.
Answer: $9.47
</example>

<problem>...</problem>

### P7 cot
Solve the word problem below and give the exact amount of change Sarah receives, in
dollars and cents.

Before answering, think step by step: what does each item cost in total, what exactly
does the coupon apply to, what base is the tax charged on, and where should rounding
happen. Show your reasoning, then give the final answer on its own line under a heading
"Answer:".

<problem>...</problem>

### P8 fullstack
You are a careful bookkeeper who checks every line of a receipt.

Goal: solve the word problem below so that the amount of change is exactly what the
register would print.

Context: this store applies coupons before tax; tax is charged on the discounted
subtotal of the whole basket; the coupon is item-specific and does not touch the pens;
amounts are rounded to the nearest cent at the tax step.

Constraints: do not estimate. Do not apply the coupon to the pens. Do not apply tax
before the discount. Show every intermediate amount. Give exactly one final answer; do
not offer alternatives.

Format: one labelled line per step (Pens, Notebooks before discount, Discount,
Notebooks after discount, Subtotal, Tax, Total, Change), then a final line exactly of
the form "Answer: $X.XX".

<problem>...</problem>

### P9 interview
Solve the word problem below and give the exact amount of change Sarah receives, in
dollars and cents. Before solving, ask me any clarifying questions you need (what the
coupon covers, when tax applies, rounding, answer format). I have answered them below;
use the answers.

<problem>...</problem>

Q: Does the 15% coupon apply to the pens as well? A: No, only the three notebooks.
Q: Is tax charged on the amount before or after the discount? A: After the discount, on
the whole discounted subtotal (pens plus discounted notebooks).
Q: How should I round? A: Keep exact values until the tax is computed, then round the
tax to the nearest cent.
Q: How do you want the answer presented? A: Show each intermediate amount, then a final
line "Answer: $X.XX".
