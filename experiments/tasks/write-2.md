# write-2: LinkedIn post on a 4-day work week (writing)

## Hidden rubric (never shown to the model under test)

Situation the prompt-writer knows: the company is Northstar Mentors, a 10-person fully
remote developer-mentorship business that moved to a 4-day week (Fridays off, same pay)
six months ago. Productivity went up (sessions delivered per person per week, about
8%), revenue is flat, team satisfaction is up and nobody has left, and there were no
unexpected problems. The post is aimed at founders and CEOs of small companies. The
founder wants it candid: no hype, no emojis, no hashtags, and it must end with one
question to readers.

Score signals (each 0-2, judge totals to 10 then normalises):
- FACTS: states all four results from the fact sheet (productivity up, revenue flat,
  satisfaction up, no unexpected problems). 2 = all four, 1 = two or three, 0 = fewer.
- HONEST: no metrics beyond those in the fact sheet (the only numbers allowed are 10
  people, 4-day, 5-day, 6 months, 8%, 3-month trial); revenue flat is said plainly, not
  spun as a win.
- VOICE: candid first-person founder voice; no hype words ("game-changer",
  "revolutionary", "transformed", "unlock"); does not open with "I'm excited to share"
  or any "excited/thrilled to announce" variant.
- FORM: 200-300 words, no hashtags, no emojis, no headline-style title line, no bullet
  list longer than 3 items.
- CLOSE: the final sentence is a single question addressed to readers, and it is the
  only question in the last paragraph.

Objective checks: word count between 200 and 300 inclusive; contains no "#" character;
contains no emoji (no code points in the Emoji ranges); last non-empty line ends with
"?"; does not contain "excited to share" (case-insensitive); contains no digit-based
number other than 10, 4, 5, 6, 8, 3 (allowing "%" after 8).

## Shared material (appears verbatim in every variant where the prompt refers to it)

<factsheet>
Company: Northstar Mentors, a fully remote developer-mentorship company. 10 people
(6 mentors, 2 operations, 2 founders).
Change: moved from a 5-day to a 4-day work week (Fridays off, same pay) six months ago,
after a 3-month trial that we then extended.
Who the post is for: founders and CEOs of small companies.
Results after six months:
- Productivity: mentoring sessions delivered per person per week went up, about 8%.
- Revenue: flat compared with the six months before the switch.
- Team satisfaction: up in our internal survey; nobody has left.
- Problems: none we did not expect. Coordinating with clients on Fridays needed a
  shared calendar note and a clear auto-reply, that was it.
What we would tell another founder: decide the metric you will watch before you start,
keep the trial fixed-length, and do not sell it internally as a perk; treat it as an
operating change.
Tone: candid, no hype, no emojis, no hashtags. End with one question to readers.
</factsheet>

## Variants

### P0 bare
Write a LinkedIn post about our switch to a 4-day week. Notes below.

<factsheet>...</factsheet>

### P1 specific
Write a LinkedIn post of about 250 words on what we learned from moving our company, a
10-person fully remote developer-mentorship business, to a 4-day work week. It is for
founders and CEOs of small companies. Use the fact sheet below.

<factsheet>...</factsheet>

### P2 role
You are a founder who writes plain-spoken LinkedIn posts that other founders actually
read to the end. Write a LinkedIn post of about 250 words on what we learned from
moving our company, a 10-person fully remote developer-mentorship business, to a 4-day
work week. It is for founders and CEOs of small companies. Use the fact sheet below.

<factsheet>...</factsheet>

### P3 context
Write a LinkedIn post of about 250 words on what we learned from moving our company, a
10-person fully remote developer-mentorship business, to a 4-day work week. It is for
founders and CEOs of small companies. Use the fact sheet below.

Background you should use: other founders ask us about this roughly once a week, and
most of them have heard only the hype version. The people reading are sceptical and
busy; they want to know what actually changed and what it cost. Our last post that
performed well was one that admitted a mistake. We are not hiring, so this is not a
recruiting post.

<factsheet>...</factsheet>

### P4 constraints
Write a LinkedIn post of about 250 words on what we learned from moving our company, a
10-person fully remote developer-mentorship business, to a 4-day work week. It is for
founders and CEOs of small companies. Use the fact sheet below.

Constraints: between 200 and 300 words. No hashtags. No emojis. Do not open with "I'm
excited to share" or any "excited/thrilled to announce" line. Do not use "game-changer",
"revolutionary", "transformed", or "unlock". Do not invent any number that is not in the
fact sheet. Say plainly that revenue was flat; do not spin it. End with exactly one
question to readers and nothing after it.

<factsheet>...</factsheet>

### P5 format
Write a LinkedIn post of about 250 words on what we learned from moving our company, a
10-person fully remote developer-mentorship business, to a 4-day work week. It is for
founders and CEOs of small companies. Use the fact sheet below.

Output format: plain text, no title line, five short paragraphs:
1. one or two sentences on what we did and when,
2. what went up (productivity, satisfaction), with the one number we have,
3. what did not change (revenue) and what problems we hit,
4. the two or three things we would tell another founder,
5. a single closing question to readers.
No hashtags, no emojis, no bullet points.

<factsheet>...</factsheet>

### P6 fewshot
Write a LinkedIn post of about 250 words on what we learned from moving our company, a
10-person fully remote developer-mentorship business, to a 4-day work week. It is for
founders and CEOs of small companies. Use the fact sheet below.

Here are two posts in the voice we want:

<example>
We dropped daily standups in March. Not because they were broken, but because nobody
could tell me what decision the last twenty had produced. We replaced them with a
written update by 10am and one thirty-minute call on Wednesdays. Three months in:
fewer interruptions, the written updates are searchable, and two people told me they
were relieved. The cost is real too. Newer hires get less ambient context, so we pair
them with someone for their first month. I would not call this a productivity win; I
would call it a trade we understand. What would you need to see before making the same
trade?
</example>

<example>
Last quarter we killed a product line that brought in about a fifth of our revenue. It
was profitable. It was also the source of most of our support tickets and the reason
our best engineer was thinking about leaving. We told customers eight weeks ahead,
refunded the ones who asked, and moved the engineer onto the core product. Revenue is
down, margin is up, the team is calmer, and I still get a slightly sick feeling when I
look at the chart. If you have shut something down that was making money, what told you
it was time?
</example>

<factsheet>...</factsheet>

### P7 cot
Write a LinkedIn post of about 250 words on what we learned from moving our company, a
10-person fully remote developer-mentorship business, to a 4-day work week. It is for
founders and CEOs of small companies. Use the fact sheet below.

Before writing, think step by step: what do sceptical founders want to know, which facts
carry the post and which are filler, what would make this read like every other 4-day
week post, and what single question would get an honest reply. Show your reasoning
briefly, then give the final post under a heading "Post:".

<factsheet>...</factsheet>

### P8 fullstack
You are a founder who writes plain-spoken LinkedIn posts that other founders actually
read to the end.

Goal: write a LinkedIn post of about 250 words on what we learned from moving our
company to a 4-day work week, so that a sceptical founder finishes it knowing exactly
what changed, what did not, and what we would do differently.

Context: we are Northstar Mentors, a 10-person fully remote developer-mentorship
business; we moved to a 4-day week six months ago after a 3-month trial. Readers are
founders and CEOs of small companies who have heard only the hype version and want
the real one. This is not a recruiting post. The fact sheet below has everything we
are willing to say publicly.

Constraints: between 200 and 300 words. No hashtags, no emojis, no title line. Do not
open with "I'm excited to share" or any "excited/thrilled to announce" line. Do not use
"game-changer", "revolutionary", "transformed", or "unlock". Do not invent any number
that is not in the fact sheet. State plainly that revenue was flat. End with exactly one
question to readers and nothing after it.

Format: plain text, five short paragraphs (what we did, what went up, what stayed flat
and what problems we hit, what we would tell another founder, one closing question).

<factsheet>...</factsheet>

### P9 interview
Write a LinkedIn post of about 250 words on what we learned from moving our company, a
10-person fully remote developer-mentorship business, to a 4-day work week. It is for
founders and CEOs of small companies. Use the fact sheet below. Before writing, ask me
any clarifying questions you need (audience, tone, numbers, length, what to avoid). I
have answered them below; use the answers.

<factsheet>...</factsheet>

Q: Who exactly is reading and what do they already believe? A: Founders and CEOs of
small companies; most have only heard the hype version and are sceptical.
Q: Can I cite numbers beyond the fact sheet? A: No. The only numbers are the ones in
the sheet; if in doubt, describe the direction rather than a figure.
Q: How should I handle revenue being flat? A: Say it plainly. Do not frame it as a win
or hide it in a subordinate clause.
Q: Tone and formatting? A: Candid, first person, no hype words, no hashtags, no emojis,
no title line, 200-300 words.
Q: Anything to avoid at the start or end? A: Do not open with "I'm excited to share".
End with exactly one question to readers and nothing after it.
Q: Is this a recruiting post? A: No, we are not hiring.
