# agent-2: Scoped plan from a vague product brief (agentic planning)

## Hidden rubric (never shown to the model under test)

Situation the prompt-writer knows: the brief is one sentence. A PM holds eight facts
(users, data source, refresh rate, auth, budget, deadline, must-haves, non-goals) that
fully determine the scope; they appear verbatim in the `<pm_answers>` block below and
are given to the model only in P3, P8 and P9. A good plan built without the facts
states its assumptions or lists the questions it would ask; a good plan built with the
facts matches them exactly.

Expected plan content when the facts are available:
- Scope: a per-account usage page behind the existing login, showing current-month
  usage per metric against the plan limit, a six-month trend per metric, CSV download
  of monthly numbers, and one email alert at 80% of a limit. Data comes from a daily
  aggregation of `usage_events` after the 03:00 UTC billing run; nothing real-time.
- Non-goals stated explicitly: invoices or billing amounts, per-user breakdown inside
  an account, public API, mobile app, custom date ranges.
- Milestones (3-6) with rough sizing that fits two engineers for six weeks, a pilot to
  20 accounts about two weeks before November 2, and general release before November
  2. A reasonable shape: (1) design plus data model and daily aggregation job, ~1.5
  weeks; (2) API and page with current-month and trend views, ~2 weeks; (3) CSV
  download and 80% alert, ~1 week; (4) pilot, fixes, release, ~1.5 weeks.
- Risks, at least three, from: aggregation job late or failing after the billing run;
  where plan limits live (the facts do not say) so limits may need a source of truth;
  querying six months from a raw event table is slow without a rollup; dashboard
  numbers disagreeing with invoices and causing support load; month boundaries and
  timezones; alert emails hitting spam or firing repeatedly; six-week budget with a
  fixed deadline leaves no slack; pilot feedback arriving too late to act on.
- Assumptions or questions for what the facts do not cover: which metrics exist and
  where plan limits are stored; whether an existing charting library or design system
  is in use; how account admins are identified in the current session model; alert
  sender and frequency; what happens for accounts with no events.

Score signals (each 0-2, judge totals to 10 then normalises):
- SCOPE: with facts, the plan includes every must-have and nothing from the non-goals,
  uses daily refresh, and sits behind the existing login (2 = all, 1 = one deviation,
  0 = more). Without facts, score on whether the plan chooses a small, explicitly
  provisional scope and labels it as such (2), or silently builds a large one (0).
- NONGOALS: has an explicit "Non-goals" (or "Out of scope") section (2 = present and,
  when facts are given, lists all five; 1 = present but incomplete; 0 = absent).
- MILESTONES: 3-6 milestones, each with a deliverable and a rough size in days or
  weeks, totalling within the budget and finishing before the deadline when the facts
  are known (2); milestones without sizing, or sizing that ignores the budget or
  deadline (1); no milestones (0).
- RISKS: at least three risks specific to this project, each with a mitigation (2);
  three or more risks but generic ("scope creep", "bugs") or without mitigations (1);
  fewer than three (0).
- ASSUMPTIONS: states assumptions or asks questions for things not covered (2 = at
  least three concrete ones; 1 = one or two; 0 = none, or invents facts as if given).

Objective checks: contains a heading or label matching "non-goals" or "out of scope"
(case-insensitive); contains "risk" (case-insensitive) and at least three bullet or
numbered items under it; contains "milestone" or a numbered list whose items each
include "week" or "day"; contains "assum" or at least one line ending with "?"; when the
facts were supplied, contains "November 2" (or "Nov 2") and does not describe invoices,
per-user breakdowns, a public API, a mobile app, or custom date ranges as in scope.

## Shared material (appears verbatim in every variant where the prompt refers to it)

<brief>
We want a dashboard so customers can see their usage.
</brief>

<pm_answers>
1. Users: about 1,200 customer accounts on paid plans. The person looking at it is
   usually the account admin, who is not technical.
2. Data source: usage events already land in a Postgres table `usage_events`
   (account_id, metric, quantity, timestamp), written by the billing pipeline. There
   is no aggregated or rollup table yet.
3. Refresh rate: daily is fine. The billing pipeline finishes by 03:00 UTC. Nobody
   needs real-time.
4. Auth: customers already log in to the existing web app (session-based). The
   dashboard must live behind that login, and an admin sees only their own account.
5. Budget: two engineers (one backend, one frontend) for six weeks, plus a designer
   for the first week. No new infrastructure spend beyond what already exists.
6. Deadline: must be in front of customers before the pricing change on November 2.
   A soft launch to 20 pilot accounts two weeks before that is wanted.
7. Must-haves: current-month usage per metric against the plan limit; last six months
   of trend per metric; CSV download of the monthly numbers; an email alert when an
   account reaches 80% of a limit (the only notification wanted).
8. Non-goals for v1: no billing or invoice display, no per-user breakdown within an
   account, no public API, no mobile app, no custom date ranges.
</pm_answers>

## Variants

### P0 bare
Make a plan for this.

<brief>...</brief>

### P1 specific
Write a scoped implementation plan for the product brief below, with milestones and
risks. It is for the engineering team that will build the first version, and it should
be short enough to review in a meeting.

<brief>...</brief>

### P2 role
You are a technical product manager who turns one-line briefs into plans engineers can
estimate. Write a scoped implementation plan for the product brief below, with
milestones and risks. It is for the engineering team that will build the first version,
and it should be short enough to review in a meeting.

<brief>...</brief>

### P3 context
Write a scoped implementation plan for the product brief below, with milestones and
risks. It is for the engineering team that will build the first version, and it should
be short enough to review in a meeting.

Background you should use: I asked the PM the questions I would normally ask and these
are the answers.

<brief>...</brief>

<pm_answers>...</pm_answers>

### P4 constraints
Write a scoped implementation plan for the product brief below, with milestones and
risks. It is for the engineering team that will build the first version, and it should
be short enough to review in a meeting.

Constraints: the brief is deliberately thin, so do not invent facts; where something is
not stated, write it down as an assumption or a question for the PM. Include an
explicit non-goals section. Give each milestone a rough size in days or weeks. List at
least three risks specific to this project, each with a mitigation; do not list generic
risks like "scope creep" without saying what would creep. Do not propose more than one
version; this is a v1 plan.

<brief>...</brief>

### P5 format
Write a scoped implementation plan for the product brief below, with milestones and
risks. It is for the engineering team that will build the first version, and it should
be short enough to review in a meeting.

Output format, with exactly these headings in this order:
"Scope (in)": bullets.
"Non-goals": bullets.
"Assumptions and open questions": bullets, each marked (assumption) or (question).
"Milestones": a table with columns #, Milestone, Deliverable, Size (days or weeks).
"Risks": three to five bullets of the form "<risk>: <mitigation>".
No introduction, no closing summary.

<brief>...</brief>

### P6 fewshot
Write a scoped implementation plan for the product brief below, with milestones and
risks. It is for the engineering team that will build the first version, and it should
be short enough to review in a meeting.

Here are two plans written from equally thin briefs, in the style we want:

<example>
Brief: "Customers want to export their data."
Scope (in): a one-click export of an account's records to a ZIP of CSVs, generated in
the background, delivered by an emailed link that expires in 7 days.
Non-goals: scheduled exports, exports of other accounts' data, PDF or XLSX formats,
partial exports by date range.
Assumptions and open questions: (assumption) an existing background job runner can be
reused; (question) which tables count as "their data" for compliance purposes?
(question) is there a size ceiling we should refuse above?
Milestones: 1. job and storage, 1 week. 2. email delivery and expiring links, 3 days.
3. UI button and status, 3 days. 4. load test on the largest account and release, 4
days.
Risks: largest accounts time out the job: chunk the export and stream to storage.
Export link leaks data if forwarded: require login to download. Export contains
personal data of other users in the account: agree the table list with legal before
milestone 1.
</example>

<example>
Brief: "We need better search."
Scope (in): replace the substring match on the records list with a ranked search over
title and notes, with type-ahead, for the existing web app.
Non-goals: search across accounts, searching file attachments, saved searches, a
search API.
Assumptions and open questions: (assumption) Postgres full-text search is enough at
current data sizes, no new search service; (question) what queries do support tickets
show users trying and failing? (question) is latency under 300 ms acceptable?
Milestones: 1. index and query, 1 week. 2. ranking and type-ahead endpoint, 1 week.
3. UI and instrumentation, 1 week. 4. compare click-through against the old search on
10% of traffic, 1 week.
Risks: ranking feels worse than substring match for exact titles: boost exact matches.
Index rebuild locks a large table: build concurrently off-peak. Type-ahead load spikes
the database: debounce and cache the top queries.
</example>

<brief>...</brief>

### P7 cot
Write a scoped implementation plan for the product brief below, with milestones and
risks. It is for the engineering team that will build the first version, and it should
be short enough to review in a meeting.

Before writing the plan, think step by step: what is the brief not telling you, which
of those gaps change the plan most, what is the smallest version that would satisfy
the sentence, what should be explicitly left out, and where is the plan most likely to
slip. Show your reasoning briefly, then give the plan under a heading "Plan:".

<brief>...</brief>

### P8 fullstack
You are a technical product manager who turns one-line briefs into plans engineers can
estimate.

Goal: write a v1 implementation plan for the brief below that the two engineers can
start on Monday, that ships to pilot accounts two weeks before the deadline, and that
leaves nothing about scope open to interpretation.

Context: I asked the PM the questions I would normally ask; the answers are below and
are the full set of facts available.

Constraints: do not invent facts beyond the PM's answers; where something is still not
stated, write it as an assumption or a question. Include an explicit non-goals section
that matches the PM's list. Give each milestone a rough size in days or weeks, and make
the total fit the budget and deadline. List at least three risks specific to this
project, each with a mitigation. Plan one version only.

Format, with exactly these headings in this order: "Scope (in)", "Non-goals",
"Assumptions and open questions" (each marked (assumption) or (question)),
"Milestones" (table: #, Milestone, Deliverable, Size), "Risks" (three to five bullets
of the form "<risk>: <mitigation>"). No introduction, no closing summary.

<brief>...</brief>

<pm_answers>...</pm_answers>

### P9 interview
Write a scoped implementation plan for the product brief below, with milestones and
risks. It is for the engineering team that will build the first version, and it should
be short enough to review in a meeting. Before writing, ask me any clarifying questions
you need (users, data, refresh, auth, budget, deadline, must-haves, non-goals). I have
answered them below; use the answers.

<brief>...</brief>

Q: Who are the users and how many? A: About 1,200 paid customer accounts; the viewer
is usually the account admin, who is not technical.
Q: Where does the usage data come from? A: A Postgres table `usage_events`
(account_id, metric, quantity, timestamp) written by the billing pipeline. No rollup
table exists yet.
Q: How fresh does it need to be? A: Daily is fine; the billing pipeline finishes by
03:00 UTC. Nobody needs real-time.
Q: How do users authenticate? A: Through the existing session-based web app login. The
dashboard sits behind it and an admin sees only their own account.
Q: What is the budget? A: Two engineers (one backend, one frontend) for six weeks, a
designer for the first week, and no new infrastructure spend.
Q: What is the deadline? A: In front of customers before the pricing change on
November 2, with a soft launch to 20 pilot accounts two weeks before that.
Q: What must v1 have? A: Current-month usage per metric against the plan limit; six
months of trend per metric; CSV download of monthly numbers; one email alert at 80% of
a limit.
Q: What is out of scope? A: Billing or invoice display, per-user breakdown within an
account, a public API, a mobile app, custom date ranges.
