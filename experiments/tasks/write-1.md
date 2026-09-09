# write-1: Customer support reply (writing)

## Hidden rubric (never shown to the model under test)

Situation the prompt-writer knows: a paying customer's CSV export failed twice in one
day; the team has confirmed a bug in the export worker and a fix is being deployed;
the customer should get an email with the fixed export within 24 hours; company
voice is warm but concise; support replies are signed "The Support Team".

Score signals (each 0-2, judge totals to 10 then normalises):
- ACK: acknowledges the frustration specifically (mentions the export failing twice).
- APOLOGY: apologises once, briefly (no groveling, no repeated apologies).
- STATUS: states that the cause is identified and being fixed (not "we are looking into it").
- NEXT: gives a concrete next step with a time ("email within 24 hours").
- FORM: under 150 words, no "limited access"/"thank you for your patience" filler, signed "The Support Team", no subject-line unless asked.

Objective checks: word count <= 150; contains "24 hours"; contains "Support Team";
does not contain "thank you for your patience".

## Shared material (appears verbatim in every variant where the prompt refers to it)

<complaint>
This is the second time today your CSV export has failed on me. I clicked Export,
waited ten minutes, and got a "something went wrong" error both times. I'm paying for
the Pro plan specifically for exports and I have a board meeting tomorrow morning. What
is going on?
</complaint>

## Variants

### P0 bare
Reply to this customer complaint.

<complaint>...</complaint>

### P1 specific
Write a reply to the customer complaint below. The customer is a paying Pro user whose
CSV export failed twice today. Keep it short.

<complaint>...</complaint>

### P2 role
You are a customer support lead at a SaaS company. Write a reply to the customer
complaint below. The customer is a paying Pro user whose CSV export failed twice today.
Keep it short.

<complaint>...</complaint>

### P3 context
Write a reply to the customer complaint below. The customer is a paying Pro user whose
CSV export failed twice today. Keep it short.

Background you should use: our engineers have confirmed a bug in the export worker and
the fix is deploying now. We will email the customer their completed export within 24
hours. Our support voice is warm but concise, and replies are signed "The Support Team".

<complaint>...</complaint>

### P4 constraints
Write a reply to the customer complaint below. The customer is a paying Pro user whose
CSV export failed twice today. Keep it short.

Constraints: under 150 words. Apologise once, briefly. Do not say "thank you for your
patience", "limited access", or "we apologise for any inconvenience". Do not ask them to
try again. Do not include a subject line. End with a concrete next step and a time.

<complaint>...</complaint>

### P5 format
Write a reply to the customer complaint below. The customer is a paying Pro user whose
CSV export failed twice today. Keep it short.

Output format: a plain-text email body with exactly four short paragraphs:
1. one sentence acknowledging what happened,
2. one sentence apologising,
3. one or two sentences on the cause and status,
4. one sentence with the next step and when. Then sign off as "The Support Team".

<complaint>...</complaint>

### P6 fewshot
Write a reply to the customer complaint below. The customer is a paying Pro user whose
CSV export failed twice today. Keep it short.

Here are two replies in the voice we want:

<example>
Complaint: "My invoice PDF shows the wrong company name. I need this fixed before I can
submit it for reimbursement."
Reply: "You're right, the PDF is pulling the old company name from your billing
profile, and that's on us. Sorry for the hassle right before a deadline. We've corrected
the record and regenerated the invoice; it's attached, and future invoices will use the
right name. If reimbursement needs anything else, reply here and we'll turn it around
same day. The Support Team"
</example>

<example>
Complaint: "Two-factor codes aren't arriving by SMS. I've been locked out for an hour."
Reply: "Being locked out for an hour is a bad way to spend a morning, and we're sorry.
Our SMS provider is having a regional outage; we've switched your account to email
codes so you can sign in right now. SMS will be restored automatically once the
provider recovers, and we'll confirm by email when it is. The Support Team"
</example>

<complaint>...</complaint>

### P7 cot
Write a reply to the customer complaint below. The customer is a paying Pro user whose
CSV export failed twice today. Keep it short.

Before writing, think step by step: what is the customer actually worried about, what do
they need to hear first, what would make this reply feel generic, and what concrete
commitment can we make. Show your reasoning briefly, then give the final reply under a
heading "Reply:".

<complaint>...</complaint>

### P8 fullstack
You are a customer support lead at a SaaS company known for warm, concise replies.

Goal: write a reply to the complaint below that leaves the customer confident their
export will be in hand before their board meeting.

Context: the customer is on the paid Pro plan; their CSV export failed twice today;
engineering has confirmed a bug in the export worker and the fix is deploying now; we
will email them the completed export within 24 hours; replies are signed "The Support
Team".

Constraints: under 150 words. Apologise once, briefly. Acknowledge the two failures
specifically. Do not say "thank you for your patience", "limited access", or "we
apologise for any inconvenience". Do not ask them to try again. No subject line.

Format: plain-text email body, four short paragraphs (acknowledge, apologise, cause and
status, next step with time), then "The Support Team".

<complaint>...</complaint>

### P9 interview
Write a reply to the customer complaint below. Before writing, ask me any clarifying
questions you need (plan, cause, timeline, voice, length). I have answered them below;
use the answers.

<complaint>...</complaint>

Q: What plan is the customer on and does it matter? A: Pro plan, paid; exports are a
Pro feature so it matters.
Q: Do we know the cause? A: Yes, a confirmed bug in the export worker; fix deploying now.
Q: What can we promise? A: We will email their completed export within 24 hours.
Q: Voice and length? A: Warm but concise, under 150 words, signed "The Support Team".
Q: Anything to avoid? A: Filler like "thank you for your patience"; don't ask them to
retry; no subject line.
