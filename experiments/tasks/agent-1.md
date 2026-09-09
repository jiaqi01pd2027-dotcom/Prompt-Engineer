# agent-1: Plan a feature for a small codebase (agentic planning)

## Hidden rubric (never shown to the model under test)

Situation the prompt-writer knows: the app is a six-file FastAPI + SQLite todo API. The
feature is an optional `due_date` on each todo plus an `overdue` filter on the list
endpoint (overdue = due date in the past and `done` is false). A correct plan changes
exactly five things: the model, a new Alembic migration, the Pydantic schemas, the list
route (and create/patch to accept the field), and the tests. `app/db.py` does not need
to change. No code can be executed; this is a plan for a developer.

Expected plan content:
- Files to touch: `app/models.py` (add nullable `due_date` datetime column),
  `alembic/versions/0002_*.py` (new revision adding the nullable column),
  `app/schemas.py` (add optional `due_date` to TodoCreate, TodoUpdate, TodoOut),
  `app/routes.py` (accept `due_date` on POST/PATCH; add `overdue` query param to
  GET /todos that filters `due_date < now AND done = false`), `tests/test_todos.py`
  (new tests). Nothing else.
- Sensible order: model and migration first (or together), then schemas, then routes,
  then tests; or tests written first against the intended API. Migration must come
  before the route is considered done. Running `alembic upgrade head` is mentioned.
- Notes that the test suite builds tables from the models directly, so the model and
  the migration must both be changed and kept in sync.
- Tests named: create with and without due_date; patch sets and clears due_date;
  overdue filter includes past-and-not-done, excludes done items with past dates,
  excludes future dates, excludes items with no due date; existing `done` filter still
  works alongside `overdue`.
- At least one risk flagged, and timezones must be one of them: naive vs aware
  datetimes, SQLite storing datetimes as text, what "now" means (server UTC), and
  clients sending local-time ISO strings. Other acceptable risks: null semantics,
  backfill of existing rows, combining filters.

Score signals (each 0-2, judge totals to 10 then normalises):
- FILES: names all five of models.py, a new alembic migration, schemas.py, routes.py,
  test_todos.py (2); misses one (1); misses two or more, or says db.py needs changes
  (0).
- NO-INVENT: does not mention any file that is not in the description (no
  services.py, config.py, frontend, Dockerfile, CI, README) (2); one invented file (1);
  more (0). Creating one new migration file is expected and does not count.
- ORDER: steps are in a workable order with the migration before the route is
  complete and tests at or near the end or explicitly test-first (2); order works but
  is unmotivated or the migration is an afterthought (1); order would not work (0).
- TESTS: names at least four of the specific test cases above and notes that tests do
  not run migrations (2); mentions tests only generically (1); no tests (0).
- RISK: flags the timezone issue with a concrete recommendation (store UTC, compare in
  UTC, accept ISO-8601 with offset) plus at least one other risk (2); mentions timezones
  without a recommendation (1); no timezone mention (0).

Objective checks: response contains "models.py", "schemas.py", "routes.py",
"test_todos.py", and "alembic" or "migration"; contains "timezone" or "time zone" or
"UTC"; contains no code block longer than 5 lines; does not contain "services.py",
"config.py", "main.py", "Dockerfile", or "README".

## Shared material (appears verbatim in every variant where the prompt refers to it)

<codebase>
Repository: todo-api (Python 3.12, FastAPI, SQLAlchemy 2.0, SQLite, Alembic, pytest).
Six files matter:

app/models.py        SQLAlchemy models. One table, `todos`, with columns id (int,
                     primary key), title (str, required), done (bool, default false),
                     created_at (datetime, UTC, set on insert).
app/schemas.py       Pydantic request/response models: TodoCreate (title),
                     TodoUpdate (title optional, done optional), TodoOut (id, title,
                     done, created_at).
app/routes.py        FastAPI router. GET /todos (optional query param `done` filters by
                     status), POST /todos, GET /todos/{id}, PATCH /todos/{id},
                     DELETE /todos/{id}. Uses the `get_db` dependency from app/db.py.
app/db.py            Engine and session factory for sqlite:///todo.db, plus the
                     `get_db` dependency. Nothing else lives here.
alembic/versions/    One migration so far, 0001_create_todos.py, which creates the
                     todos table. `alembic upgrade head` applies migrations in
                     production. The test suite does NOT run migrations: it uses a
                     fresh in-memory SQLite database and creates tables directly
                     from the models.
tests/test_todos.py  pytest plus FastAPI TestClient. Twelve tests cover create, list,
                     list filtered by `done`, get, patch, delete. All green.
</codebase>

## Variants

### P0 bare
How would I add due dates to this app?

<codebase>...</codebase>

### P1 specific
Write an implementation plan (steps only, no code) for adding an optional due date to
each todo in the app described below, plus an `overdue` filter on GET /todos where
overdue means the due date is in the past and the todo is not done. The plan is for a
developer who will implement it.

<codebase>...</codebase>

### P2 role
You are a senior backend engineer who writes implementation plans that a junior
developer can follow without asking questions. Write an implementation plan (steps
only, no code) for adding an optional due date to each todo in the app described below,
plus an `overdue` filter on GET /todos where overdue means the due date is in the past
and the todo is not done. The plan is for a developer who will implement it.

<codebase>...</codebase>

### P3 context
Write an implementation plan (steps only, no code) for adding an optional due date to
each todo in the app described below, plus an `overdue` filter on GET /todos where
overdue means the due date is in the past and the todo is not done. The plan is for a
developer who will implement it.

Background you should use: the app is already deployed with real rows in `todo.db`, so
existing todos must keep working with no due date. Clients are a web UI and a mobile
app in different time zones, and they send timestamps as ISO-8601 strings. The team
runs `alembic upgrade head` on deploy and CI runs pytest on every push. The API shape
the team agreed on is a `due_date` field on create, patch and responses, and
`?overdue=true` on the list endpoint.

<codebase>...</codebase>

### P4 constraints
Write an implementation plan (steps only, no code) for adding an optional due date to
each todo in the app described below, plus an `overdue` filter on GET /todos where
overdue means the due date is in the past and the todo is not done. The plan is for a
developer who will implement it.

Constraints: only reference files that exist in the description, plus one new migration
file. Do not write code; describe changes in prose. Do not skip the database migration.
Do not leave testing as a single "add tests" step; name the cases. Flag at least one
risk and say how to handle it. Do not propose new dependencies, services, or a
frontend.

<codebase>...</codebase>

### P5 format
Write an implementation plan (steps only, no code) for adding an optional due date to
each todo in the app described below, plus an `overdue` filter on GET /todos where
overdue means the due date is in the past and the todo is not done. The plan is for a
developer who will implement it.

Output format: a numbered list of steps, each one line of the form
"N. <file path>: <what changes>", followed by a section "Tests:" listing test cases as
bullets (one line each), then a section "Risks:" with bullets of the form
"<risk>: <how to handle it>". No code blocks, no introduction, no closing summary.

<codebase>...</codebase>

### P6 fewshot
Write an implementation plan (steps only, no code) for adding an optional due date to
each todo in the app described below, plus an `overdue` filter on GET /todos where
overdue means the due date is in the past and the todo is not done. The plan is for a
developer who will implement it.

Here are two plans for other features in this codebase, in the style we want:

<example>
Feature: add a `priority` field (low, normal, high; default normal).
1. app/models.py: add `priority` string column, not null, default "normal".
2. alembic/versions/0002_add_priority.py: add the column with a server default so
   existing rows are backfilled.
3. app/schemas.py: add `priority` to TodoCreate (optional, default normal), TodoUpdate
   (optional) and TodoOut; validate against the three allowed values.
4. app/routes.py: no filter changes; create and patch pass the field through.
5. tests/test_todos.py: create with default priority, create with explicit priority,
   reject an invalid value, patch priority; note tests build tables from models so the
   model change alone makes them pass, the migration is checked by running
   `alembic upgrade head` locally.
Risks: an invalid value slipping through if validation is only in the schema and not
the model; agree it lives in the schema.
</example>

<example>
Feature: search todos by title substring.
1. app/routes.py: add optional query param `q` to GET /todos, filter with a
   case-insensitive LIKE; combine with the existing `done` filter.
2. app/schemas.py, app/models.py: no changes.
3. No migration needed.
4. tests/test_todos.py: match on substring, case-insensitive match, no match returns
   empty list, `q` combined with `done`.
Risks: LIKE with user input needs the wildcard characters escaped; SQLite LIKE is
case-insensitive only for ASCII.
</example>

<codebase>...</codebase>

### P7 cot
Write an implementation plan (steps only, no code) for adding an optional due date to
each todo in the app described below, plus an `overdue` filter on GET /todos where
overdue means the due date is in the past and the todo is not done. The plan is for a
developer who will implement it.

Before writing the plan, think step by step: which layers does a new persisted field
pass through in this app, what has to change in each file, what does "in the past"
mean on a server, what can go wrong with existing rows, and how the tests will prove
the filter works. Show your reasoning briefly, then give the plan under a heading
"Plan:".

<codebase>...</codebase>

### P8 fullstack
You are a senior backend engineer who writes implementation plans that a junior
developer can follow without asking questions.

Goal: produce a step-by-step plan (no code) for adding an optional `due_date` to each
todo in the app described below and an `overdue` filter on GET /todos, so that the
developer can implement it in one sitting and the tests prove it works.

Context: the app is deployed with real rows in `todo.db`, so existing todos must keep
working with no due date. Clients are a web UI and a mobile app in different time
zones sending ISO-8601 timestamps. The team runs `alembic upgrade head` on deploy and
pytest in CI. Agreed API: `due_date` on create, patch and responses; `?overdue=true` on
the list endpoint, where overdue means due date in the past and not done.

Constraints: only reference files in the description plus one new migration file. Do
not write code. Do not skip the migration. Name the test cases individually. Flag at
least one risk with a mitigation. Do not propose new dependencies, services, or a
frontend.

Format: numbered steps, each "N. <file path>: <what changes>"; then "Tests:" with one
bullet per case; then "Risks:" with bullets of the form "<risk>: <how to handle it>".
No introduction or closing summary.

<codebase>...</codebase>

### P9 interview
Write an implementation plan (steps only, no code) for adding an optional due date to
each todo in the app described below, plus an `overdue` filter on GET /todos where
overdue means the due date is in the past and the todo is not done. The plan is for a
developer who will implement it. Before writing, ask me any clarifying questions you
need (field type, API shape, migrations, timezones, testing). I have answered them
below; use the answers.

<codebase>...</codebase>

Q: Is the due date required, and is it a date or a datetime? A: Optional and nullable;
a datetime, because the mobile app shows times.
Q: How do clients send it and how should it be stored? A: ISO-8601 strings, possibly
with an offset. Store in UTC; treat naive values as UTC.
Q: What exactly is "overdue"? A: `due_date` earlier than the current UTC time and `done`
is false. Items with no due date are never overdue.
Q: What is the API shape? A: `due_date` on POST and PATCH bodies and in responses;
`?overdue=true` on GET /todos, combinable with the existing `done` filter.
Q: Do I need a migration? A: Yes, a new Alembic revision. Remember the tests do not run
migrations; they build tables from the models.
Q: How thorough should the tests be? A: Name each case: with and without due date,
patch sets and clears it, overdue includes past-and-not-done, excludes done, excludes
future, excludes null.
