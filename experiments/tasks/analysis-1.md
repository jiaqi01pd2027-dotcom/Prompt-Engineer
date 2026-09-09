# analysis-1: Meeting transcript to decisions and action items (analysis)

## Hidden rubric (never shown to the model under test)

Situation the prompt-writer knows: the transcript is a 30-minute product sync for a
scheduling app called Lumen. Exactly five decisions were made and exactly six action
items were assigned, each to one named owner with a due date. Everything else is
chit-chat or an explicit non-decision.

Expected decisions (5):
- D1: Calendar sync beta ships with Google Calendar only; Outlook is out of scope for the beta.
- D2: Beta launch date moves from October 1 to October 6.
- D3: Team plan price rises from $8 to $10 per seat for new customers from November 1; existing customers stay at $8 (grandfathered).
- D4: The weekly sync moves from Monday to Wednesday, same time, starting next week.
- D5: The workspace feature is officially named "Rooms" (not "Spaces").

Expected action items (6), owner and due date:
- A1: Mei: final onboarding mock-ups (Outlook tile removed or greyed out), due Thursday.
- A2: Dan: written beta rollout runbook (flags, rollback), due Friday.
- A3: Raj: beta usage dashboard (sync success rate, conflicts per user), due October 3.
- A4: Sofia: post the top 20 calendar-sync tickets in #product, due Tuesday.
- A5: Tom: draft the pricing-change email to existing customers, due next Wednesday.
- A6: Priya: update the roadmap doc and send it to leadership, due end of week.

Distractors that must NOT appear as decisions or action items:
- "We might look at Outlook in Q1" (explicitly a maybe, not decided).
- "Someone should look at the competitor pricing page" (explicitly unowned).
- "Outlook coming soon" label on the page (a wording allowance, not a decision; if listed at all it must be folded into D1 rather than counted separately).
- Anything about headsets, coffee, the tape, or meeting twice this week.

Score signals (each 0-2, judge totals to 10 then normalises):
- DECISIONS: recall of D1-D5 (2 = all five with the key specifics: Google-only, Oct 6, $10/new customers/Nov 1, Wednesday, Rooms; 1 = three or four; 0 = fewer).
- ACTIONS: recall of A1-A6 with the correct owner (2 = all six owners correct; 1 = four or five; 0 = fewer). A due date wrong or missing costs nothing here but see FORM.
- NO-INVENT: no item that is not in the lists above, and no distractor listed as a decision or action (2 = clean, 1 = one extra, 0 = two or more).
- ATTRIB: no owner swapped (e.g. runbook assigned to Raj, dashboard to Dan); due dates present and correct for at least five of six actions.
- FORM: two labelled lists (decisions, action items), one line per item, no narrative summary, no "key themes", no preamble, under 200 words total.

Objective checks: word count <= 200 excluding the two list headings; contains
"Rooms", "October 6" (or "Oct 6" / "6 October"), "Wednesday", "$10" (or "10 dollars"),
"Google"; each of Mei, Dan, Raj, Sofia, Tom, Priya appears at least once; does not
contain "Q1" as a decision line; does not contain "competitor" in an action line.

## Shared material (appears verbatim in every variant where the prompt refers to it)

<transcript>
Lumen product sync, Monday 14 September, 10:02

Priya: Okay, I think we have everyone. Dan, is your mic working this time?

Dan: It is. New headset. The old one finally died on Thursday.

Mei: The one held together with tape?

Dan: Rest in peace.

Priya: Alright. Housekeeping: the coffee machine on four is fixed, so stop stealing from three. Tom, that means you.

Tom: I have no idea what you're talking about.

Priya: Sure. Okay, main item is the calendar sync beta. Dan, where are we?

Dan: Google side is basically done. Two-way sync works, conflicts are handled, retry queue is in. Outlook is another story. The API permissions took two weeks and we still get token refresh failures on maybe one in twenty accounts. No fix yet.

Priya: So if we hold the beta for Outlook, what does that do to the date?

Dan: Honestly, it pushes it into October, maybe late October. If we go Google-only I can be ready by the sixth.

Sofia: I pulled the ticket tags last week. Roughly eighty percent of sync requests are Google Calendar. Outlook is mostly the two enterprise trials.

Tom: The enterprise trials are exactly who I'd want to impress, though.

Priya: I hear that, but I won't hold eighty percent of demand for a flaky twenty. Decision: the beta ships with Google only; Outlook is out of scope for this beta. We revisit after we see beta data.

Tom: Fine. Can we at least say "Outlook coming soon" on the page?

Priya: "Coming soon" is fine as long as we don't put a date on it.

Dan: Agreed. So the date is the sixth. I'll note that the original plan said the first. We're formally moving beta launch to October 6.

Priya: Yes, that's the decision. October 6, Google only.

Mei: Does that change the onboarding flow? I have the mock-ups half done with an Outlook tile in them.

Priya: Drop the tile, or grey it out with the coming soon label. Can you get me the final onboarding mock-ups by Thursday?

Mei: Thursday is fine if nobody adds anything else to my plate this week.

Tom: No promises.

Mei: Tom.

Priya: Mei owns final onboarding mock-ups, Thursday. Dan, I'd also like a written rollout runbook for the beta, who flips what flag, rollback steps, the usual. Can that be Friday?

Dan: Friday works. I'll draft it tomorrow and have Raj sanity check the monitoring section.

Priya: Great, Dan owns the runbook, due Friday. Raj, on that note, we need to actually see what beta users are doing. Can you build a beta usage dashboard, sync success rate, conflicts per user, that kind of thing?

Raj: Yes. I need the event names from Dan but I can have a first version by October 3, that gives a few days before launch to fix whatever is broken in it.

Priya: Raj, beta usage dashboard, October 3. Perfect.

Sofia: Speaking of tickets, I have a lot of sync-related feedback sitting in the queue from before the beta even existed. Do you want that?

Priya: Yes. Pull the top twenty tickets about calendar sync and post them in the product channel. Tuesday?

Sofia: Tuesday is doable.

Priya: Sofia, top twenty sync tickets in #product by Tuesday. Next: pricing. Tom, you had the numbers.

Tom: Short version: the Team plan at eight dollars a seat is underpriced against every competitor. Finance modelled ten. Churn risk looked small if we grandfather existing customers.

Priya: And the recommendation was new customers only?

Tom: New customers only, starting November 1. Existing customers stay at eight until at least next year, and we tell them that proactively so nobody panics.

Dan: I have no engineering concerns, the plan IDs are already separate.

Priya: Then let's call it. Team plan goes to ten dollars per seat for new customers from November 1. Existing customers are grandfathered at eight. Tom, can you draft the email to existing customers explaining this? Next Wednesday is fine, it doesn't go out until October anyway.

Tom: Draft by next Wednesday, yes.

Priya: Tom owns the pricing email draft, next Wednesday. Okay, a quick one. This meeting on a Monday keeps colliding with the support handover and Dan's on-call review.

Dan: And with my will to live.

Priya: Noted. I'm proposing we move this sync to Wednesdays, same time. Any objections?

Mei: Wednesday is better for me actually.

Sofia: Same.

Priya: Done. Weekly sync moves to Wednesday from next week.

Raj: Does that mean this week we meet twice?

Priya: No, Raj, it means we skip Monday and meet Wednesday.

Raj: Just checking.

Priya: Last thing, naming. The workspace feature. Engineering says Spaces, Mei's mock-ups say Rooms, and support says "the folder thing".

Sofia: To be fair, customers call it the folder thing.

Mei: Rooms tested better in the five user interviews, people understood you invite someone into a room. Spaces sounded like storage.

Tom: Rooms is also easier to say in a sentence. "Create a room for the launch."

Priya: Any objection to Rooms? No? Then we go with Rooms, officially, everywhere. I'll update the roadmap doc with everything from today, the date change, the scope, pricing, the name, and send it to leadership by end of week.

Dan: Can you also add a line that we might look at Outlook in Q1? Not committing, just so it's on the page.

Priya: I'll add it as a maybe. Not deciding that today.

Tom: Someone should also look at the competitor pricing page again at some point, they changed it last month.

Priya: At some point, yes. Nobody's owning that right now. Okay, that's everything. Enjoy the coffee on four.

Dan: Enjoy the new headset.

Mei: Enjoy Tom not touching my mock-ups.

Priya: Meeting ended 10:31.
</transcript>

## Variants

### P0 bare
Summarise this meeting.

<transcript>...</transcript>

### P1 specific
Read the meeting transcript below and produce two lists: the decisions that were made,
and the action items with the owner and due date for each. Include only things that
were actually decided or assigned in the meeting.

<transcript>...</transcript>

### P2 role
You are an experienced chief of staff who takes precise, minimal meeting minutes. Read
the meeting transcript below and produce two lists: the decisions that were made, and
the action items with the owner and due date for each. Include only things that were
actually decided or assigned in the meeting.

<transcript>...</transcript>

### P3 context
Read the meeting transcript below and produce two lists: the decisions that were made,
and the action items with the owner and due date for each. Include only things that
were actually decided or assigned in the meeting.

Background you should use: this is the weekly product sync for Lumen, a scheduling app.
Priya is the product manager and runs the meeting; Dan leads engineering; Mei is the
designer; Tom runs marketing; Sofia leads support; Raj is the data analyst. The notes
go to leadership, who only read them to learn what changed and who is doing what next;
they do not need the discussion. The team distinguishes between a decision (Priya
states it as settled) and things people float as "maybe" or "someone should".

<transcript>...</transcript>

### P4 constraints
Read the meeting transcript below and produce two lists: the decisions that were made,
and the action items with the owner and due date for each. Include only things that
were actually decided or assigned in the meeting.

Constraints: one line per item. Every action item must name exactly one owner and a due
date; if nobody was assigned, it is not an action item. Do not include ideas that were
explicitly deferred or left unowned. Do not add a narrative summary, themes, or
"next steps" beyond the two lists. Do not paraphrase numbers, dates, or names; copy
them as said. Under 200 words.

<transcript>...</transcript>

### P5 format
Read the meeting transcript below and produce two lists: the decisions that were made,
and the action items with the owner and due date for each. Include only things that
were actually decided or assigned in the meeting.

Output format:

Decisions
1. <what was decided, with the specific values (dates, prices, names)>
...

Action items
1. <Owner>: <task> (due <date>)
...

Nothing before or after the two lists.

<transcript>...</transcript>

### P6 fewshot
Read the meeting transcript below and produce two lists: the decisions that were made,
and the action items with the owner and due date for each. Include only things that
were actually decided or assigned in the meeting.

Here is the style we want, from a different meeting:

<example>
Transcript excerpt: "Lena: So we're agreed, the mobile app drops support for iOS 14 in
the March release. Omar, can you write the deprecation notice by the 20th? Omar: Sure.
Lena: And someone should probably check the crash stats for iOS 15 at some point."
Output:
Decisions
1. Mobile app drops iOS 14 support in the March release.
Action items
1. Omar: write the iOS 14 deprecation notice (due the 20th)
</example>

<example>
Transcript excerpt: "Kai: I'd love to move the retro to Fridays but let's not decide
now. Anna: Okay. I'll send the survey results to the team tonight anyway."
Output:
Decisions
(none)
Action items
1. Anna: send the survey results to the team (due tonight)
</example>

<transcript>...</transcript>

### P7 cot
Read the meeting transcript below and produce two lists: the decisions that were made,
and the action items with the owner and due date for each. Include only things that
were actually decided or assigned in the meeting.

Before answering, think step by step: go through the transcript in order, note each
moment where something is stated as settled versus merely floated, and each moment
where a named person accepts a task with a date. Check that nothing you list was
explicitly deferred or left without an owner. Show your reasoning briefly, then give
the final lists under a heading "Minutes:".

<transcript>...</transcript>

### P8 fullstack
You are an experienced chief of staff who takes precise, minimal meeting minutes.

Goal: turn the transcript below into minutes that let leadership see in under a minute
what changed and who is doing what next.

Context: this is the weekly product sync for Lumen, a scheduling app. Priya is the
product manager and runs the meeting; Dan leads engineering; Mei is the designer; Tom
runs marketing; Sofia leads support; Raj is the data analyst. A decision is something
Priya states as settled; "maybe", "at some point" and "someone should" are not
decisions or action items.

Constraints: one line per item. Every action item names exactly one owner and a due
date. Do not include deferred or unowned ideas. Do not paraphrase numbers, dates, or
names. No narrative summary, themes, or preamble. Under 200 words.

Format:
Decisions
1. <what was decided, with the specific values>
Action items
1. <Owner>: <task> (due <date>)
Nothing else.

<transcript>...</transcript>

### P9 interview
Read the meeting transcript below and produce minutes. Before writing, ask me any
clarifying questions you need (audience, what counts as a decision, how to handle
unowned tasks, format, length). I have answered them below; use the answers.

<transcript>...</transcript>

Q: Who reads these minutes and what for? A: Leadership, to see what changed and who
owns what next. They do not want the discussion.
Q: What counts as a decision? A: Something Priya states as settled. "Maybe", "at some
point", "not deciding today" are not decisions.
Q: What if a task has no owner or no date? A: Then it is not an action item; leave it
out.
Q: Format? A: Two lists, "Decisions" and "Action items", one line each; action items as
"Owner: task (due date)". Nothing else.
Q: Length? A: Under 200 words. Keep the specific numbers, dates and names exactly as
said.
