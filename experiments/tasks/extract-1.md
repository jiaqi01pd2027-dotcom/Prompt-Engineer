# extract-1: Feedback lines to ticket titles (extraction)

## Hidden rubric (never shown to the model under test)

Situation the prompt-writer knows: the support team files every piece of feedback as a
ticket whose title starts with one of six fixed area labels (Billing, Login, Export,
Mobile, Notifications, Performance) in square brackets, followed by a brief
description, under 60 characters in total, one title per feedback line, in the same
order as the input. Titles are scanned in a queue, so they must be concrete (what broke,
where) and never generic ("Bug report", "User issue").

Expected area per line, and the detail each title must carry:

| # | expected area | must mention |
|---|---|---|
| 1 | Billing | duplicate/double charge (the $29 is optional) |
| 2 | Login | Google sign-in and the loop/redirect back to login |
| 3 | Export | PDF export and the cut-off/missing last column |
| 4 | Mobile | iPhone (or iOS/mobile) nav bar covering/hiding the Save button |
| 5 | Notifications | repeated/duplicate emails for comments already read |
| 6 | Performance | dashboard slow to load with many projects (20s and/or 100+ projects optional) |

Reference titles (one acceptable answer; wording may differ):
1. [Billing] Duplicate $29 charge on monthly subscription
2. [Login] Google sign-in loops back to login page
3. [Export] PDF export cuts off last table column
4. [Mobile] iPhone bottom nav bar hides Save button
5. [Notifications] Repeat emails for already-read comments
6. [Performance] Dashboard takes 20s+ with 100+ projects

Wrong-area traps: line 2 is Login, not "Integrations" or "Google"; line 4 is Mobile,
not "UI" or "Editor"; line 5 is Notifications, not "Email"; line 6 is Performance, not
"Dashboard".

Score signals (each 0-2, judge totals to 10 then normalises):
- AREA: correct area label on each of the six lines (2 = 6/6, 1 = 4-5, 0 = fewer).
- FORMAT: every line matches "[Area] description" exactly, with the label from the fixed list, one space after the bracket, no trailing period (2 = all six, 1 = one deviation, 0 = more).
- LENGTH: every title is under 60 characters (2 = all six, 1 = one over, 0 = more).
- DETAIL: each title carries the "must mention" detail above and is specific, not generic (2 = all six, 1 = four or five, 0 = fewer).
- FORM: exactly six lines in input order and nothing else: no numbering, no preamble, no explanation, no blank-line commentary, no code fence.

Objective checks: output has exactly 6 non-empty lines; each line matches
`^\[(Billing|Login|Export|Mobile|Notifications|Performance)\] \S.*$`; each line length
< 60; the sequence of labels equals [Billing, Login, Export, Mobile, Notifications,
Performance]; no line ends with "."; output contains no lines starting with a digit or
"-".

## Shared material (appears verbatim in every variant where the prompt refers to it)

<feedback>
1. I got charged twice this month for the same subscription, my card statement shows two $29 charges on the 3rd.
2. Every time I try to sign in with Google it just spins for a bit and then dumps me back on the login page.
3. The PDF export cuts off the last column of my table, it's been like this since the update last week.
4. On my iPhone the bottom navigation bar covers the Save button so I literally can't save anything.
5. I keep getting email notifications for comments I've already read, like five a day, it's driving me nuts.
6. The dashboard takes 20+ seconds to load now that I have more than a hundred projects.
</feedback>

## Variants

### P0 bare
Make tickets out of these.

<feedback>...</feedback>

### P1 specific
Turn each of the six user-feedback lines below into a support ticket title. Each title
must be in the format "[Area] brief description", where Area is one of: Billing, Login,
Export, Mobile, Notifications, Performance. Keep every title under 60 characters, one
title per line, in the same order as the input.

<feedback>...</feedback>

### P2 role
You are a support triage lead who writes crisp ticket titles that engineers can act on
without opening the ticket. Turn each of the six user-feedback lines below into a
support ticket title. Each title must be in the format "[Area] brief description", where
Area is one of: Billing, Login, Export, Mobile, Notifications, Performance. Keep every
title under 60 characters, one title per line, in the same order as the input.

<feedback>...</feedback>

### P3 context
Turn each of the six user-feedback lines below into a support ticket title. Each title
must be in the format "[Area] brief description", where Area is one of: Billing, Login,
Export, Mobile, Notifications, Performance. Keep every title under 60 characters, one
title per line, in the same order as the input.

Background you should use: the titles go straight into a triage queue that engineers
scan in a narrow sidebar, which is why they are capped at 60 characters. The area label
routes the ticket: Billing goes to the payments team, Login covers any sign-in method
including Google and SSO, Export covers PDF/CSV output, Mobile covers anything on the
iOS or Android apps, Notifications covers in-app and email alerts, Performance covers
slowness and timeouts. A good title says what broke and where; "Bug" or "User issue"
is useless.

<feedback>...</feedback>

### P4 constraints
Turn each of the six user-feedback lines below into a support ticket title. Each title
must be in the format "[Area] brief description", where Area is one of: Billing, Login,
Export, Mobile, Notifications, Performance. Keep every title under 60 characters, one
title per line, in the same order as the input.

Constraints: exactly six lines, nothing before or after them. Do not number the lines,
do not add bullets, do not wrap them in a code block. Do not invent an area outside the
six listed. Do not end titles with a period. Do not use vague words like "issue",
"problem" or "bug" on their own; name the thing that broke. Do not include the user's
emotions or phrases like "user reports".

<feedback>...</feedback>

### P5 format
Turn each of the six user-feedback lines below into a support ticket title. Each title
must be in the format "[Area] brief description", where Area is one of: Billing, Login,
Export, Mobile, Notifications, Performance. Keep every title under 60 characters, one
title per line, in the same order as the input.

Output format: plain text, six lines, each line exactly
[Area] <description>
with one space after the closing bracket, no numbering, no trailing punctuation, no
blank lines, no headings, no explanation.

<feedback>...</feedback>

### P6 fewshot
Turn each of the six user-feedback lines below into a support ticket title. Each title
must be in the format "[Area] brief description", where Area is one of: Billing, Login,
Export, Mobile, Notifications, Performance. Keep every title under 60 characters, one
title per line, in the same order as the input.

Examples of the conversion we want:

<example>
Feedback: "My invoice says I'm on the Team plan but I downgraded to Basic two months ago
and I'm still being billed the higher amount."
Title: [Billing] Still billed Team price after downgrade to Basic
</example>

<example>
Feedback: "Search on the Android app crashes the whole thing if I type more than about
ten characters."
Title: [Mobile] Android search crashes on queries over 10 chars
</example>

<example>
Feedback: "Password reset emails take almost an hour to arrive, by then the link has
expired."
Title: [Login] Password reset email arrives after link expires
</example>

<feedback>...</feedback>

### P7 cot
Turn each of the six user-feedback lines below into a support ticket title. Each title
must be in the format "[Area] brief description", where Area is one of: Billing, Login,
Export, Mobile, Notifications, Performance. Keep every title under 60 characters, one
title per line, in the same order as the input.

Before answering, think step by step for each line: what actually broke, which of the
six areas owns that, and what is the shortest concrete phrasing that fits under 60
characters. Show your reasoning briefly, then give the six titles under a heading
"Titles:" with nothing else after them.

<feedback>...</feedback>

### P8 fullstack
You are a support triage lead who writes crisp ticket titles that engineers can act on
without opening the ticket.

Goal: convert the six feedback lines below into ticket titles that route correctly and
read clearly in the triage sidebar.

Context: the sidebar truncates at 60 characters. The area label routes the ticket:
Billing to payments; Login covers any sign-in method including Google and SSO; Export
covers PDF/CSV output; Mobile covers anything on the iOS or Android apps; Notifications
covers in-app and email alerts; Performance covers slowness and timeouts. A good title
says what broke and where.

Constraints: exactly six lines in input order, nothing before or after. Area must be
one of Billing, Login, Export, Mobile, Notifications, Performance. Under 60 characters
each. No numbering, bullets, code block, trailing period, or vague words like "issue"
or "bug" on their own. Do not include the user's emotions.

Format: plain text, each line exactly "[Area] <description>" with one space after the
closing bracket.

<feedback>...</feedback>

### P9 interview
Turn the six user-feedback lines below into support ticket titles. Before writing, ask
me any clarifying questions you need (title format, allowed areas, length, ordering,
what to leave out). I have answered them below; use the answers.

<feedback>...</feedback>

Q: What format should each title have? A: "[Area] brief description", one space after
the bracket, no trailing period.
Q: Which area labels are allowed? A: Only Billing, Login, Export, Mobile,
Notifications, Performance. Login includes Google sign-in; Mobile includes anything on
the iPhone app; Notifications includes notification emails; Performance is slowness.
Q: Is there a length limit? A: Under 60 characters per title.
Q: Same order as the input, one per line? A: Yes, exactly six lines, nothing else, no
numbering.
Q: Should I keep the user's tone? A: No. Just what broke and where.
