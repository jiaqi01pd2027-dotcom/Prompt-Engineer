# analysis-2: Compare three project tools for a small team (analysis)

## Hidden rubric (never shown to the model under test)

Situation the prompt-writer knows: the three tools are fictional and the datasheets in
the shared material are the only source of truth. The team is 8 people today, may grow
to 10, needs a Gantt/timeline view and a native GitHub integration, wants monthly
billing (no annual commitment), and has a hard budget of $100 per month.

Ground-truth facts the judge checks against:
- Planlet: Gantt is Business-only. Business is $15/user monthly ($12 annual). Monthly
  cost for 8 users = $120, for 10 = $150 (annual: $96 / $120). Team plan ($8 monthly)
  has no Gantt. Native GitHub: yes (Team and above). Minimum 3 seats.
- Taskforge: Pro is $9/user/month with no annual discount. 8 users = $72, 10 = $90.
  Gantt: yes. Native GitHub: yes (also GitLab). Guests count as seats. Time tracking
  built in. Storage 100 GB. API limit 1,000 requests/hour.
- Hivemind Boards: Starter is $49/month flat for up to 10 users (Growth $99 up to 25).
  Gantt: yes. Native GitHub: no (Slack, Google Drive, Zapier only). Storage 25 GB.
  1,000 automation runs/month. Max 5 guests. An 11th user forces the Growth plan.

Expected recommendation: Taskforge Pro. It is the only tool that meets all three
requirements (Gantt, native GitHub, monthly billing under $100 at both 8 and 10 users).
Planlet is ruled out because Gantt requires Business, which exceeds the budget on
monthly billing ($120 at 8 users, $150 at 10). Hivemind is the cheapest ($49 flat) and
has Gantt but has no native GitHub integration; it is an acceptable runner-up only if the
answer explicitly says the GitHub requirement would have to go through Zapier.

For P0 only (no requirements stated): score REC as 2 if the answer either recommends
Taskforge or explicitly conditions the choice on needs (e.g. "Hivemind if cost matters
most, Taskforge if you need GitHub"); score 0 if it recommends Planlet without noting
the Gantt/Business restriction. FACTS scoring is unchanged.

Score signals (each 0-2, judge totals to 10 then normalises):
- FACTS: every price, limit, and feature stated matches the datasheets (2 = no errors, 1 = one error, 0 = two or more). Common errors: giving Planlet Gantt on Team, giving Hivemind native GitHub, using Planlet annual prices as if monthly, pricing Hivemind per seat.
- COST: computes the monthly cost at 8 and 10 users for each tool, or at minimum for the recommended tool and its nearest rival ($72/$90 Taskforge, $49 Hivemind, $120/$150 Planlet Business).
- REC: recommends Taskforge Pro and states why the other two fail a requirement.
- COVERAGE: addresses all three of features, limits (users, storage, guests, automations, API), and pricing for all three tools.
- FORM: comparison is easy to scan (table or parallel bullets), the recommendation is stated once and clearly, under 400 words, no filler about "it depends on your needs" without then answering.

Objective checks: word count <= 400; contains "Taskforge"; contains "$49"; contains
"$72" or "$90"; contains "Business" (Planlet plan name); does not contain any price
string absent from the datasheets ("$5", "$7", "$10/user", "$11", "$20"); does not
contain "Hivemind" and "GitHub" in the same sentence without "Zapier", "no", "not",
"lacks", or "missing" in that sentence.

## Shared material (appears verbatim in every variant where the prompt refers to it)

<tools>
PLANLET (planlet.example)
Plans: Free (up to 5 users, 3 projects). Team: $6 per user/month billed annually, or $8
per user/month billed monthly. Business: $12 per user/month billed annually, or $15 per
user/month billed monthly. Paid plans require a minimum of 3 seats. 14-day trial of
Business.
Views: Kanban, list and calendar on all paid plans. Gantt/timeline view on Business only.
Integrations: Slack, GitHub, Google Drive (Team and above).
Automations: 250 runs per month on Team; unlimited on Business.
Storage: 10 GB per workspace on Team; 100 GB on Business.
Guests: unlimited free guests (view and comment only).
Time tracking: not available.

TASKFORGE (taskforge.example)
Plans: Free (up to 3 users, 2 projects). Pro: $9 per user/month, same price on monthly
or annual billing. No minimum seats. 30-day trial.
Views: Kanban, list, calendar and Gantt on Pro.
Integrations: Slack, GitHub, GitLab, Figma.
Automations: unlimited.
Storage: 100 GB per workspace.
Guests: guests count as full paid seats.
Time tracking: built in.
API: 1,000 requests per hour per workspace.

HIVEMIND BOARDS (hivemindboards.example)
Plans: Starter: $49 per month flat for up to 10 users. Growth: $99 per month flat for up
to 25 users. Annual billing gives two months free. 14-day trial. Adding an 11th user on
Starter requires upgrading to Growth.
Views: Kanban, calendar and Gantt on all plans.
Integrations: Slack, Google Drive, Zapier. No native GitHub or GitLab integration.
Automations: 1,000 runs per month on Starter; 5,000 on Growth.
Storage: 25 GB on Starter; 100 GB on Growth.
Guests: up to 5 free guests.
Time tracking: only via a Zapier connection to a third-party tracker.
</tools>

## Variants

### P0 bare
Which of these project tools is best?

<tools>...</tools>

### P1 specific
Compare the three project management tools described below for a team of 8 people that
may grow to 10, and recommend one. The team needs a Gantt/timeline view and a native
GitHub integration, wants monthly billing with no annual commitment, and can spend at
most $100 per month. Cover features, limits and pricing, and say why you rule out the
other two.

<tools>...</tools>

### P2 role
You are a software-team operations consultant who has helped dozens of small teams
choose tooling and who is careful to quote vendor facts exactly. Compare the three
project management tools described below for a team of 8 people that may grow to 10,
and recommend one. The team needs a Gantt/timeline view and a native GitHub
integration, wants monthly billing with no annual commitment, and can spend at most
$100 per month. Cover features, limits and pricing, and say why you rule out the other
two.

<tools>...</tools>

### P3 context
Compare the three project management tools described below for a team of 8 people that
may grow to 10, and recommend one. The team needs a Gantt/timeline view and a native
GitHub integration, wants monthly billing with no annual commitment, and can spend at
most $100 per month. Cover features, limits and pricing, and say why you rule out the
other two.

Background you should use: the team is a product squad of 6 engineers, 1 designer and 1
product manager; two contractors may join for a quarter, which is where the 10 comes
from. They plan sprints on a timeline, and every task links to a GitHub pull request,
so Gantt and GitHub are must-haves rather than nice-to-haves. They were burned by an
annual contract last year and finance will only approve monthly billing. They rarely
use automations and have about 5 GB of attachments. The datasheets are the only
information available; do not assume features that are not listed.

<tools>...</tools>

### P4 constraints
Compare the three project management tools described below for a team of 8 people that
may grow to 10, and recommend one. The team needs a Gantt/timeline view and a native
GitHub integration, wants monthly billing with no annual commitment, and can spend at
most $100 per month. Cover features, limits and pricing, and say why you rule out the
other two.

Constraints: use only facts from the datasheets; do not invent features, prices or
limits, and do not draw on what you know about real products. Quote monthly-billing
prices, not annual ones, and show the monthly total at both 8 and 10 users for each
tool. Make exactly one recommendation; do not end with "it depends". Under 400 words.
Do not include a generic introduction about the importance of choosing tools.

<tools>...</tools>

### P5 format
Compare the three project management tools described below for a team of 8 people that
may grow to 10, and recommend one. The team needs a Gantt/timeline view and a native
GitHub integration, wants monthly billing with no annual commitment, and can spend at
most $100 per month. Cover features, limits and pricing, and say why you rule out the
other two.

Output format:
1. A markdown table with one row per tool and these columns: Tool, Plan needed, Monthly
   cost at 8 users, Monthly cost at 10 users, Gantt, Native GitHub, Key limits.
2. A heading "Recommendation" followed by one sentence naming the tool and plan.
3. A heading "Why not the others" with one bullet per rejected tool.
No other sections.

<tools>...</tools>

### P6 fewshot
Compare the three project management tools described below for a team of 8 people that
may grow to 10, and recommend one. The team needs a Gantt/timeline view and a native
GitHub integration, wants monthly billing with no annual commitment, and can spend at
most $100 per month. Cover features, limits and pricing, and say why you rule out the
other two.

Here is the kind of comparison we want, from a different evaluation:

<example>
Requirement: 4-person team, needs SSO, budget $40/month.
Datasheets: Alpha $12/user (SSO on all plans); Beta $5/user (SSO on Enterprise only,
$25/user); Gamma $30 flat up to 5 users (no SSO).
Output:
| Tool | Plan needed | Cost at 4 users | SSO |
| Alpha | Standard | $48 | yes |
| Beta | Enterprise | $100 | yes |
| Gamma | Flat | $30 | no |
Recommendation: none of the three meets both requirements; Alpha is the closest
(SSO, $8 over budget). Beta's SSO plan is 2.5x the budget; Gamma has no SSO at all.
</example>

<example>
Requirement: 12-person team, needs a mobile app, monthly billing.
Datasheets: Delta $7/user monthly (mobile app); Echo $60 flat up to 10 users then $90
up to 20 (mobile app); Foxtrot $6/user annual only (mobile app).
Output:
| Tool | Plan needed | Cost at 12 users | Mobile | Monthly billing |
| Delta | Pro | $84 | yes | yes |
| Echo | Tier 2 | $90 | yes | yes |
| Foxtrot | Standard | $72 | yes | no |
Recommendation: Delta Pro. Foxtrot is cheapest but annual-only, which fails the billing
requirement; Echo costs $6 more than Delta and its tier jump at 10 users makes growth
more expensive.
</example>

<tools>...</tools>

### P7 cot
Compare the three project management tools described below for a team of 8 people that
may grow to 10, and recommend one. The team needs a Gantt/timeline view and a native
GitHub integration, wants monthly billing with no annual commitment, and can spend at
most $100 per month. Cover features, limits and pricing, and say why you rule out the
other two.

Before answering, think step by step: for each tool, identify which plan is the
cheapest one that actually has Gantt and native GitHub, then compute the monthly cost
at 8 and at 10 users on monthly billing, then check that cost against the $100 budget,
and only then compare the remaining candidates on limits. Show your reasoning briefly,
then give the final comparison and recommendation under a heading "Recommendation:".

<tools>...</tools>

### P8 fullstack
You are a software-team operations consultant who has helped dozens of small teams
choose tooling and who is careful to quote vendor facts exactly.

Goal: recommend one of the three tools below so the team can sign up this week with
confidence that it meets their requirements and budget.

Context: the team is a product squad of 6 engineers, 1 designer and 1 product manager,
with two contractors possibly joining for a quarter (so 8 users now, 10 at peak). They
plan sprints on a timeline and every task links to a GitHub pull request, so a
Gantt/timeline view and a native GitHub integration are must-haves. Finance will only
approve monthly billing, at most $100 per month. They rarely use automations and have
about 5 GB of attachments. The datasheets are the only information available.

Constraints: use only facts from the datasheets; do not invent features, prices or
limits, and do not draw on real products. Quote monthly-billing prices and show the
monthly total at 8 and at 10 users for each tool. Make exactly one recommendation; do
not end with "it depends". Under 400 words. No generic introduction.

Format:
1. A markdown table with columns: Tool, Plan needed, Monthly cost at 8 users, Monthly
   cost at 10 users, Gantt, Native GitHub, Key limits.
2. A heading "Recommendation" with one sentence naming the tool and plan.
3. A heading "Why not the others" with one bullet per rejected tool.
No other sections.

<tools>...</tools>

### P9 interview
Compare the three project management tools described below for my team and recommend
one. Before answering, ask me any clarifying questions you need (team size, must-have
features, billing, budget, how much detail you want). I have answered them below; use
the answers.

<tools>...</tools>

Q: How big is the team, and will it change? A: 8 people now; two contractors may join
for a quarter, so plan for 10.
Q: Which features are must-haves? A: A Gantt/timeline view and a native GitHub
integration. Everything else is nice-to-have.
Q: Monthly or annual billing? A: Monthly only. Finance will not approve an annual
commitment.
Q: Budget? A: $100 per month, hard cap, at both 8 and 10 users.
Q: Do you use automations or need lots of storage? A: Rarely, and about 5 GB.
Q: How should I present it? A: A short comparison covering features, limits and pricing
for all three, then one clear recommendation and why the other two are out. Use only
what the datasheets say. Under 400 words.
