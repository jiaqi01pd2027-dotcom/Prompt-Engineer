# extract-2: Receipts to structured JSON (extraction)

## Hidden rubric (never shown to the model under test)

Situation the prompt-writer knows: the five receipts feed an expense tool that needs,
for each receipt, the merchant name, the date the payment was made (ISO 8601
YYYY-MM-DD), the total amount actually paid as a plain number (no currency symbol;
currencies are deliberately mixed and are not converted), and one category from a
fixed list: Food, Transport, Office, Software, Travel. Each receipt contains traps:
a US-style date (03/14/2026), European decimal commas (23,50), a subtotal/net that is
not the total, a future renewal date that is not the payment date, and a hotel folio
with check-in/check-out dates where the payment date is the departure date.

Expected output (exact):

[
  {"name": "Blue Fern Cafe", "date": "2026-03-14", "amount": 18.40, "category": "Food"},
  {"name": "CityCab Taxi", "date": "2026-03-14", "amount": 25.50, "category": "Transport"},
  {"name": "Paperworks Ltd", "date": "2026-02-28", "amount": 50.00, "category": "Office"},
  {"name": "Notemark Inc.", "date": "2026-04-01", "amount": 96.00, "category": "Software"},
  {"name": "Harbor View Inn", "date": "2026-02-27", "amount": 216.00, "category": "Travel"}
]

Per-receipt traps and the wrong answers they produce:
1. amount 18.4 (not 4.90 or the tip line); date 2026-03-14 (not 2026-14-03).
2. amount 25.5 (not 23.5 fare, not 2350); date 2026-03-14 from "Sat 14 Mar 2026".
3. amount 50 (not 41.67 net or 8.33 VAT); date from "Date of issue".
4. date 2026-04-01 (not 2027-04-01 renewal, not 2026-03-31 period end); amount 96.
5. date 2026-02-27 (paid on departure; not 2026-02-25 arrival, not 2026-02-05 or
   2026-05-02 from misreading DD.MM); amount 216 (not 105, not 0.00 balance due).

Score signals (each 0-2, judge totals to 10 then normalises):
- VALID: output is a single JSON array of exactly five objects with exactly the four keys name, date, amount, category (2 = valid and clean, 1 = valid but with extra keys or wrapped in prose/code fence, 0 = invalid or not an array).
- DATES: all five dates exactly as expected (2 = 5/5, 1 = 4/5, 0 = fewer).
- AMOUNTS: all five amounts numerically equal to expected, as JSON numbers not strings (2 = 5/5, 1 = 4/5, 0 = fewer).
- NAMES+CATS: merchant names match after normalisation (lowercase, punctuation removed, whitespace collapsed) and categories exactly match (2 = 10/10 fields, 1 = 8-9, 0 = fewer).
- FORM: the JSON is the only content (no explanation, no markdown headings; a bare ```json fence is tolerated), objects in receipt order, keys in the order name, date, amount, category.

Objective checks: `json.loads` on the output (after stripping an optional ```json fence)
succeeds and yields a list of length 5; each element is a dict with exactly the keys
{name, date, amount, category}; `date` matches `^\d{4}-\d{2}-\d{2}$` and equals the
expected value; `amount` is int or float (not str) and `abs(amount - expected) < 0.005`;
`category` equals the expected string; `name` equals the expected name after
normalisation; order matches the receipts.

## Shared material (appears verbatim in every variant where the prompt refers to it)

<receipts>
=== Receipt 1 ===
*** BLUE FERN CAFE ***
12 Larch St    Tel 555-0142
03/14/2026  08:12    Cashier: 04
Flat white              4.90
Avocado toast          11.50
Orange juice            2.00
SUBTOTAL               18.40
TIP                     0.00
TOTAL                 $18.40
VISA ****4471  APPROVED
THANK YOU FOR VISITING!
Rate us online for a free coffee

=== Receipt 2 ===
CityCab Taxi - Trip receipt
Ride ID 7F3K-22
Pickup: Sat 14 Mar 2026 22:41, Northgate Station
Dropoff: 23:03, 8 Elm Row
Fare   EUR 23,50
Tip    EUR  2,00
Total charged: €25,50
Paid with saved card. No signature required.
Questions? help@citycab.example

=== Receipt 3 ===
PAPERWORKS LTD            VAT REG GB 402 1188 73
Invoice/Receipt no. PW-018842
Date of issue: 2026-02-28        Due: on receipt
2 x A4 copier paper (box) ........ 29.98
1 x Stapler, heavy duty ........... 11.69
Net                                 41.67
VAT 20%                              8.33
TOTAL GBP                           50.00
PAID IN FULL - card
Returns within 28 days with this receipt

=== Receipt 4 ===
Notemark Inc.
Receipt #NM-55120
Thanks for your purchase!
Item: Notemark Pro (annual)
Billing period: 1 Apr 2026 - 31 Mar 2027
Billed on: April 1, 2026
Amount paid: US$96.00 (incl. $0.00 tax)
Next renewal: April 1, 2027 for US$96.00
Manage your subscription at notemark.example/account

=== Receipt 5 ===
HARBOR VIEW INN
Folio 3391    Room 214
Guest: J. Okafor
Arrival 25.02.2026    Departure 27.02.2026
25.02  Room night          105.00
26.02  Room night          105.00
27.02  City tax              6.00
       Balance             216.00
Paid 27.02.2026 by Mastercard   216.00
Balance due: 0.00
We hope you enjoyed your stay
</receipts>

## Variants

### P0 bare
Pull the data out of these receipts as JSON.

<receipts>...</receipts>

### P1 specific
Extract the following from each of the five receipts below and return a JSON array with
one object per receipt, in order: "name" (the merchant), "date" (the date the payment
was made, in ISO 8601 YYYY-MM-DD), "amount" (the total actually paid, as a number with
no currency symbol), and "category" (one of: Food, Transport, Office, Software,
Travel).

<receipts>...</receipts>

### P2 role
You are a meticulous bookkeeper who processes expense receipts and never confuses a
subtotal with a total. Extract the following from each of the five receipts below and
return a JSON array with one object per receipt, in order: "name" (the merchant),
"date" (the date the payment was made, in ISO 8601 YYYY-MM-DD), "amount" (the total
actually paid, as a number with no currency symbol), and "category" (one of: Food,
Transport, Office, Software, Travel).

<receipts>...</receipts>

### P3 context
Extract the following from each of the five receipts below and return a JSON array with
one object per receipt, in order: "name" (the merchant), "date" (the date the payment
was made, in ISO 8601 YYYY-MM-DD), "amount" (the total actually paid, as a number with
no currency symbol), and "category" (one of: Food, Transport, Office, Software,
Travel).

Background you should use: these were photographed by staff travelling in the US, the
EU and the UK, so dates appear in US (MM/DD/YYYY), European (DD.MM.YYYY) and written
forms, and some amounts use a decimal comma. Currencies are mixed and must not be
converted; only the number matters. The expense tool cares about when the card was
charged, so for a hotel that is the departure/checkout date and for a subscription it
is the billed-on date, not the next renewal. The categories are: Food (cafes,
restaurants), Transport (taxis, trains, fuel), Office (stationery, supplies), Software
(subscriptions, licences), Travel (hotels, flights).

<receipts>...</receipts>

### P4 constraints
Extract the following from each of the five receipts below and return a JSON array with
one object per receipt, in order: "name" (the merchant), "date" (the date the payment
was made, in ISO 8601 YYYY-MM-DD), "amount" (the total actually paid, as a number with
no currency symbol), and "category" (one of: Food, Transport, Office, Software,
Travel).

Constraints: return only the JSON array, no prose before or after it. Amounts must be
JSON numbers, not strings, and must be the total charged, never a subtotal, net, tax,
fare-before-tip or "balance due" line. Do not convert currencies. Do not use renewal
dates, billing-period end dates or check-in dates as the payment date. Do not add keys
beyond the four requested. Do not invent a category outside the five listed.

<receipts>...</receipts>

### P5 format
Extract the following from each of the five receipts below and return a JSON array with
one object per receipt, in order: "name" (the merchant), "date" (the date the payment
was made, in ISO 8601 YYYY-MM-DD), "amount" (the total actually paid, as a number with
no currency symbol), and "category" (one of: Food, Transport, Office, Software,
Travel).

Output format: exactly this shape and nothing else, keys in this order:

[
  {"name": "<merchant>", "date": "YYYY-MM-DD", "amount": 0.00, "category": "<Food|Transport|Office|Software|Travel>"},
  ...
]

Five objects, valid JSON, no comments, no trailing commas, no surrounding text.

<receipts>...</receipts>

### P6 fewshot
Extract the following from each of the five receipts below and return a JSON array with
one object per receipt, in order: "name" (the merchant), "date" (the date the payment
was made, in ISO 8601 YYYY-MM-DD), "amount" (the total actually paid, as a number with
no currency symbol), and "category" (one of: Food, Transport, Office, Software,
Travel).

Examples of the extraction we want:

<example>
Receipt: "RAILNORTH e-ticket / Leeds to York / Travel date 02.05.2026 / Purchased
30.04.2026 / Fare GBP 14,20 / Booking fee 1,00 / Total paid GBP 15,20"
Output: {"name": "Railnorth", "date": "2026-04-30", "amount": 15.20, "category": "Transport"}
</example>

<example>
Receipt: "Cloudnest Backup - Invoice / Plan: 2 TB monthly / Charged on 11/02/2025
(US) / Subtotal $9.99 / Tax $0.80 / Total $10.79 / Next charge 12/02/2025"
Output: {"name": "Cloudnest Backup", "date": "2025-11-02", "amount": 10.79, "category": "Software"}
</example>

<receipts>...</receipts>

### P7 cot
Extract the following from each of the five receipts below and return a JSON array with
one object per receipt, in order: "name" (the merchant), "date" (the date the payment
was made, in ISO 8601 YYYY-MM-DD), "amount" (the total actually paid, as a number with
no currency symbol), and "category" (one of: Food, Transport, Office, Software,
Travel).

Before answering, think step by step for each receipt: which of the dates on it is the
payment date and what format is it in, which line is the total actually charged (as
opposed to subtotals, tax, fares before tip, or balances), and which category the
merchant belongs to. Show your reasoning briefly, then give the final JSON array under a
heading "JSON:".

<receipts>...</receipts>

### P8 fullstack
You are a meticulous bookkeeper who processes expense receipts and never confuses a
subtotal with a total.

Goal: produce a JSON array the expense tool can import directly, one object per receipt
below, in order.

Context: the receipts were photographed by staff in the US, the EU and the UK, so dates
appear in US (MM/DD/YYYY), European (DD.MM.YYYY) and written forms, and some amounts
use a decimal comma. Currencies are mixed and must not be converted. The tool cares
about when the card was charged: for a hotel that is the checkout date, for a
subscription the billed-on date, never the next renewal. Categories: Food (cafes,
restaurants), Transport (taxis, trains, fuel), Office (stationery, supplies), Software
(subscriptions, licences), Travel (hotels, flights).

Constraints: JSON only, no prose. Amounts are JSON numbers, always the total charged,
never a subtotal, net, tax, fare-before-tip or balance-due line. Exactly four keys per
object. Category must be one of the five listed.

Format, keys in this order:
[
  {"name": "<merchant>", "date": "YYYY-MM-DD", "amount": 0.00, "category": "<category>"},
  ...
]

<receipts>...</receipts>

### P9 interview
Extract structured data from the five receipts below as JSON. Before answering, ask me
any clarifying questions you need (which fields, date rules, which amount, categories,
currency handling, output shape). I have answered them below; use the answers.

<receipts>...</receipts>

Q: Which fields do you want? A: name (merchant), date, amount, category. Nothing else.
Q: Which date, and in what format? A: The date the payment was charged, as YYYY-MM-DD.
For the hotel that is the checkout date; for the subscription it is the billed-on date,
not the renewal.
Q: Which amount? A: The total actually paid. Never the subtotal, net, tax, fare before
tip, or a "balance due" line.
Q: How do I handle different currencies and decimal commas? A: Do not convert. Just
give the number, so "23,50" becomes 23.5.
Q: What categories are allowed? A: Food, Transport, Office, Software, Travel.
Q: Output shape? A: One JSON array, five objects in receipt order, keys name, date,
amount, category, no text around it.
