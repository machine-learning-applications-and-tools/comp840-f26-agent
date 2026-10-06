# Week 4: The planner

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

`week03-README.md` is new this week. Week 3 came out before the
per-week file names, so your `README.md` still holds Week 3's
instructions. The pull above replaces `README.md` with the new index and
adds `week03-README.md`, so Week 3's instructions are kept under their
own name.

Do not add `agent/loop.py` or `agent/tools.py` to that list. They are
your own work from Week 3, and pulling them would replace it with that
week's stub.

## What is here

```
agent/
    __init__.py     makes this a package
    config.py       the model name. Only place it appears.
    llm.py          generate(), with rate limiting and retries
    tools.py        the tools your agent can use
    loop.py         your Week 3 loop. Do not change it.
    planner.py      THE PLANNER. This is the lab.
    cli.py          command line entry point, now with --plan
demo_one_turn.py    Week 3's demo, still here for reference
demo_plan_only.py   watch a raw plan come back, before you parse one
demo_react_vs_plan.py   the same task, run reactively (ReAct) and planned,
                        back to back. See "Reactive vs. planned" below.
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

Week 3's loop is not a rough draft of this week's idea. It is the other
standard way to structure an agent. Deciding one step at a time, with no
separate planning phase, is called ReAct. This week's design, writing the
whole plan first, is usually called plan-then-execute. Neither one is
always right. `demo_react_vs_plan.py` runs one task both ways so you can
see the difference before you build it:

```bash
python demo_react_vs_plan.py
```

## The lab

### 1. Write the planner

Open `agent/planner.py`. Two functions, both empty, both explained in their
own docstrings:

- `make_plan(task)`: one call to the model, no tools attached, asking for a
  numbered plan. Returns the plan as a list of strings.
- `run_with_plan(task, ...)`: gets the plan, folds it into the task text,
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

`tasks.py` has six tasks, each needing at least three tool calls in a
row, using some mix of `list_files`, `search_files`, `read_file` and
`calculator`. Run your planner on at least three of them. The loop will
not always follow the plan exactly. Notice when it does not, but you do
not need to fix it.

### 3. Compare all six

`agent/planner.py` has a `compare(task)` function at the bottom. It is
given, so you can focus on the planner above it. Read it: it runs the
same task reactively (`run()`) and planned (`run_with_plan()`), and
prints both answers and what each one cost in calls and tokens.

Run `compare()` on **all six** tasks from `tasks.py`. This is required
for everyone, COMP840 and COMP740. Planning does not win every time.
Across six tasks you should see a mix: some where it wins, some where it
loses, and at least one near-tie. That spread is the finding, not any
single result. `week04-OUTPUT.md` says exactly what to write up.

### 4. Answer the questions

In `week04-OUTPUT.md`.

## Extension

Required for COMP840. Optional but encouraged for COMP740.

Planning decides the order before anything runs. There is a third,
separate step: decide whether to trust the *result* after it runs, and
retry once if it does not hold up. This is sometimes called "Reflexion."
After `compare()`, `agent/planner.py` has a `reflect(task)` stub. Finish
`compare()` on all six tasks first and check your quota before starting
this one, since a critique-and-retry costs at least two more calls on top
of whatever `run_with_plan()` alone needs.

## Do not change the entry point

`python -m agent.cli --task "..."` has to keep working exactly as it does
now. `--plan` is new and optional. It does not replace the default
behavior. In Week 12 you will run each other's agents, and that only works
if they are all invoked the same way.

## Watch your quota

15 requests a minute, 500 a day. A planned run costs at least one more
call than a reactive one, the planning call, on top of whatever the loop
needs. `MAX_STEPS` also caps how many calls a run can make.

`compare()` runs a task twice, so six tasks is roughly 60-80+ calls total,
depending on how many steps each run takes. That is comfortably inside the
daily limit, but at 15 requests a minute it takes a while. Do not
leave it until the last hour before the deadline.

If something goes wrong, stop it with Ctrl+C rather than letting it run.

## Submitting

Fill in `week04-OUTPUT.md` and commit everything, including your code.

**Due 11:59pm Monday.**
