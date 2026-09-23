# Week 4 — The planner

COMP840 / COMP740 · ML Applications and Tools

New here? Start with the top-level `README.md` for one-time setup and
`UPDATING.md` for how to pull weekly updates. This file is this week's
instructions only.

## Pulling this week's files

```bash
git fetch upstream
git checkout upstream/main -- README.md UPDATING.md week03-README.md week04-README.md week04-OUTPUT.md agent/cli.py agent/planner.py tasks.py demo_plan_only.py demo_react_vs_plan.py
git add -A
git commit -m "Pull Week 4 update"
```

`week03-README.md` is new this week specifically -- Week 3 shipped
before this per-week naming existed, so your existing `README.md`
currently holds Week 3's specific instructions. Pulling the file list
above replaces `README.md` with the new stable index and adds
`week03-README.md` alongside it, so Week 3's instructions are still
there under their own name, not lost.

Do not add `agent/loop.py` or `agent/tools.py` to that list -- those are
your own completed work from Week 3, and pulling them would overwrite it
with that week's stub.

## What is here

```
agent/
    __init__.py     makes this a package
    config.py       the model name. Only place it appears.
    llm.py          generate(), with rate limiting and retries
    tools.py        the tools your agent can use
    loop.py         Week 3's loop. Done -- do not change it.
    planner.py      THE PLANNER. This is the lab.
    cli.py          command line entry point, now with --plan
demo_one_turn.py    Week 3's demo, still here for reference
demo_plan_only.py   watch a raw plan come back, before you parse one
demo_react_vs_plan.py   the same task, run reactively (ReAct) and planned,
                        back to back -- see "Reactive vs. planned" below
tasks.py            six tasks that need three or more tools in sequence
```

Everything works except `planner.py`.

## Run this first

```bash
python demo_plan_only.py
```

One API call. It makes the exact call `make_plan()` has to make, by hand,
so you see what a real reply looks like before you write code that has to
parse it.

## The idea

Week 3's loop reacts one step at a time: call the model, see if it wants a
tool, run the tool, repeat. It works, but the model never has more than the
next single step in view.

This week, before any tool runs, the model writes a short plan for itself.
Then Week 3's loop runs exactly as it already does, except the plan is
sitting in the conversation the whole time, so every tool-choosing step can
see it and follow it. You are not changing `loop.py`. You are changing what
it gets handed.

## Reactive vs. planned

Week 3's loop is not a rough draft of this week's idea -- it is the other
legitimate way to structure an agent. Deciding one step at a time, with no
separate planning phase, has a name: ReAct. This week's design, writing the
whole plan up front, is usually called plan-then-execute. Neither is
"correct"; `demo_react_vs_plan.py` runs one task both ways so you can see
the difference before you build either side of it yourself:

```bash
python demo_react_vs_plan.py
```

## The lab

### 1. Write the planner

Open `agent/planner.py`. Two functions, both empty, both explained in their
own docstrings:

- `make_plan(task)` — one call to the model, no tools attached, asking for a
  numbered plan. Returns the plan as a list of strings.
- `run_with_plan(task, ...)` — gets the plan, folds it into the task text,
  and hands that straight to `loop.run()`.

Test it with a task from `tasks.py`:

```bash
python -m agent.cli --task "$(python -c 'from tasks import TASKS; print(TASKS[0])')" --plan
```

Or shorter, from a Python shell:

```python
from agent.planner import run_with_plan
from tasks import TASKS
print(run_with_plan(TASKS[0]))
```

### 2. Try it on all six

`tasks.py` has six tasks, each needing at least three tool calls in
sequence — some mix of `list_files`, `search_files`, `read_file`, and
`calculator`. Run your planner against at least three of them. Not every
plan needs to be followed exactly by the loop underneath it — that is worth
noticing, not fixing.

### 3. Compare all six

`agent/planner.py` has a `compare(task)` function at the bottom, already
written — this week's focus is the planner above it, not a stats-diffing
harness, so it's given rather than a third thing to implement. Read it: it
runs the same task both reactive (`run()`) and planned (`run_with_plan()`),
and prints the answers and the cost (calls, tokens) of each.

Run `compare()` on **all six** tasks from `tasks.py` — required for
everyone, COMP840 and COMP740 both. Planning does not win every time.
Across six tasks you should see a real mix: some where it wins, some
where it loses, and at least one near-tie. That spread is the finding,
not any single result — see `week04-OUTPUT.md` for exactly what to write up.

### 4. Answer the questions

In `week04-OUTPUT.md`.

## Extension

Required for COMP840. Optional but encouraged for COMP740.

Planning decides the order before anything runs. There is a third,
separate move: decide whether to trust the *result* after it runs, and
retry once if it does not hold up — sometimes called "Reflexion." Past
`compare()`, `agent/planner.py` has a `reflect(task)` stub. Finish
`compare()` on all six tasks first and check your quota before starting
this one, since a critique-and-retry costs at least two more calls on top
of whatever `run_with_plan()` alone needs.

## Do not change the entry point

`python -m agent.cli --task "..."` has to keep working exactly as it does
now. `--plan` is new and optional; it does not replace the default
behavior. In Week 12 you will run each other's agents, and that only works
if they are all invoked the same way.

## Watch your quota

15 requests a minute, 500 a day. A planned run costs at least one more call
than a reactive one — the planning call itself — on top of whatever the
loop underneath it needs. `MAX_STEPS` still exists partly to protect you
from yourself.

`compare()` runs a task twice, so six tasks is roughly 60-80+ calls total,
depending on how many steps each run takes. That is comfortably inside the
daily limit, but it will take real wall-clock time at 15 requests a
minute — do not leave this until the last hour before the deadline.

If something goes wrong, stop it with Ctrl+C rather than letting it run.

## Submitting

Fill in `week04-OUTPUT.md` and commit everything, including your code.

**Due 11:59pm Monday.**
