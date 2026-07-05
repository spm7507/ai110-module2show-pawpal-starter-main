# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Today's Schedule
================
08:00 AM — Give medication (10 min) [priority: high] for Whiskers
08:10 AM — Morning walk (30 min) [priority: high] for Rex
08:40 AM — Feed breakfast (15 min) [priority: medium] for Rex
08:55 AM — Play time (20 min) [priority: low] for Whiskers


```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

The domain logic in `pawpal_system.py` is covered by unit tests in `tests/test_pawpal.py`.

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
tests/test_pawpal.py ...................x..............          [100%]

======================== 33 passed, 1 xfailed in 0.02s =========================
```

### What the suite covers

The tests focus on the scheduling behaviors most likely to break, including these required cases:

| Behavior | Test |
|----------|------|
| **Sorting correctness** — items come back in chronological order | `test_sort_by_time_orders_schedule_chronologically` |
| **Recurrence logic** — completing a daily task creates the next day's task | `test_complete_task_auto_queues_next_occurrence` |
| **Conflict detection** — two tasks at the same time are flagged | `test_detect_conflicts_flags_duplicate_start_times` |

Beyond those, the suite exercises edge cases: half-open overlap boundaries
(back-to-back tasks don't clash), midnight wraparound, in-day recurrence spacing,
zero-duration and exact-budget tasks, unassigned-pet conflicts, malformed times,
and empty-scheduler safety.

> **One `xfail`:** `test_priority_dominates_over_duration_for_very_long_tasks`
> documents a known limitation — `Task.priority_score()` weights priority by
> `×1000`, so a task longer than ~1000 minutes can be out-sorted by a
> lower-priority one. The test is marked `xfail(strict=True)`, so it will alert
> us if the scoring is ever fixed.


Confidence Level:

My confidence level is about a 4.5 all the test passed so I am too worried about but sometimes there is always a loop hole in tests. Overall this is my confidence level for the test results.

## 📐 Smarter Scheduling

Each scheduling feature and the method in `pawpal_system.py` that implements it:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| **Priority sorting** | `Scheduler.sort_tasks()` | Orders tasks by `Task.priority_score()` (priority first, shorter duration as tie-breaker). |
| **Time sorting (tasks)** | `Scheduler.sort_tasks_by_time()` | Orders tasks by their `Task.time` attribute; untimed tasks sort last. |
| **Time sorting (schedule)** | `Scheduler.sort_by_time()` | Orders generated `ScheduledItem`s chronologically by start time. |
| **Filtering by pet / status** | `Scheduler.filter_tasks(pet=, pet_name=, completed=)` | Narrows the task pool by pet object, case-insensitive pet name, and/or completion status. |
| **Schedule building** | `Scheduler.generate_schedule()` | Greedy fit: places highest-priority tasks that fit the owner's available minutes; skips completed tasks by default. |
| **Conflict detection** | `Scheduler.find_conflicts()` | Returns overlapping `ScheduledItem` pairs as `Conflict`s; `Conflict.same_pet` flags same-pet vs. cross-pet clashes. |
| **Conflict reporting** | `Scheduler.detect_conflicts()`, `Scheduler.explain_conflicts()` | Raw `(earlier, later)` pairs, and a human-readable multi-line report. |
| **Lightweight conflict warning** | `Scheduler.conflict_warning()` | Returns a one-line warning string (or `None` if clear) and never raises — safe for UI use. |
| **Recurring tasks (within a day)** | `Task.is_recurring()`, `Scheduler.generate_schedule()` | `interval_minutes` + `occurrences` repeat a task several times in one day (e.g. meds every 8h). |
| **Recurring tasks (daily / weekly)** | `Task.next_occurrence()`, `Scheduler.complete_task()` | Completing a `recurrence="daily"`/`"weekly"` task auto-creates the next dated instance. |

## 📸 Demo Walkthrough

Main UI description:

1. Launch the streamlit app with 'stream lit run app.py.'
Owner & Pets: sets the owner's name, they would be able to choose how many minutes they have to care for today: They would be able to as


Tasks: the owner would be able to add a title for the task, duration, prioriity and which pet to assign to. The task is sorted by the highest priority.


Biild Schedule:

First we must click generate schedule. Then the app would show a "conflict warning"(or elese "no conflict").

**Example workflow:**

1. Launch the app with `streamlit run app.py`.
2. Under **Owner & Pets**, set the owner's name (e.g. Jordan) and available minutes (e.g. 120) — the time budget the scheduler fits tasks into.
3. Add a pet (e.g. `Mochi`, dog, 3) and click **Add pet**; it appears in the list with its current task count.
4. Add tasks — e.g. *Morning walk* (20 min, high) and *Play time* (20 min, low) — and assign them to a pet. The task list sorts highest-priority first, and you can filter it by pet or status.
5. Click **Generate schedule** to see today's plan, any conflict warnings, and the reasoning behind each choice.

**Key Scheduler behaviors shown:**

- **Priority sorting** — the task list and the generated plan lead with the highest-priority tasks, with shorter duration breaking ties.
- **Time sorting** — the plan is displayed in chronological order by start time.
- **Filtering** — tasks can be narrowed by pet (case-insensitive name) and by completion status (All / Pending / Completed).
- **Greedy scheduling** — only tasks that fit the owner's remaining minutes are placed; completed tasks are skipped by default.
- **Conflict warnings** — overlapping tasks are flagged as same-pet vs. cross-pet, with a UI-safe one-line warning plus an expandable detailed report.
- **Explanations** — each placed task is justified, and skipped tasks note that there wasn't enough remaining time.

**Sample CLI output** — the command-line demo in `main.py` exercises the same logic without Streamlit:

```bash
python main.py
```

```
Tasks sorted by time
====================
07:00 AM — Give medication (10 min) [priority: high] for Whiskers
07:30 AM — Feed breakfast (15 min) [priority: medium] for Rex
08:00 AM — Morning walk (30 min) [priority: high] for Rex
05:00 PM — Play time (20 min) [priority: low] for Whiskers

Rex's tasks
===========
- Morning walk (30 min) [priority: high] for Rex
- Feed breakfast (15 min) [priority: medium] for Rex

Outstanding tasks (not yet done)
================================
- Play time (20 min) [priority: low] for Whiskers
- Morning walk (30 min) [priority: high] for Rex
- Give medication (10 min) [priority: high] for Whiskers

Today's Schedule
================
08:00 AM — Give medication (10 min) [priority: high] for Whiskers
08:10 AM — Morning walk (30 min) [priority: high] for Rex
08:40 AM — Play time (20 min) [priority: low] for Whiskers

Conflict Check
==============
⚠️ 1 scheduling conflict(s) detected (1 cross-pet) — consider freeing time or rescheduling.
Found 1 conflict(s):
  Conflict [different pets]: 'Morning walk' (08:00–08:30) overlaps 'Give medication' (08:00–08:10)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
