# Week 13: Evaluation and benchmarking

COMP840 / COMP740 · ML Applications and Tools

New here? Start with the top-level `README.md` for one-time setup and
`UPDATING.md` for how to pull weekly updates. This file is this week's
instructions only.

## Pulling this week's files

Commit your own Week 11 work first. Then:

```bash
git fetch upstream
git checkout upstream/main -- README.md week13-README.md week13-OUTPUT.md agent/evaluate.py eval_cases.py demo_evaluate.py tasks.py
git add -A
git commit -m "Pull Week 13 update"
```

What each one is for:

- `week13-README.md`, `week13-OUTPUT.md`, `agent/evaluate.py`,
  `eval_cases.py` and `demo_evaluate.py` are new this week.
- `README.md` gains one line pointing to this file.
- `tasks.py` has a new docstring saying how this week uses it. The six
  tasks are the same.

Nothing else you already have changes this week. Do not add `agent/loop.py`,
`agent/tools.py`, `agent/planner.py`, `agent/memory.py`,
`agent/retrieval.py`, `agent/sandbox.py`, `agent/delegate.py` or
`agent/team.py` to that list. Those are your own work from Weeks 3 to 11,
and pulling them would overwrite it.

If you skipped the Week 11 pull, do that one first, from
`week11-README.md`.

## What is here

```
agent/
    loop.py, planner.py, memory.py, retrieval.py, sandbox.py,
    delegate.py, team.py
                    your work from Weeks 3 to 11. Do not change them.
    evaluate.py     this week's lab
eval_cases.py       one case per task in tasks.py: the expected answer,
                    and what a sensible run should do on the way there
demo_evaluate.py    same answer, different runs, checked two ways.
                    0 API calls.
tasks.py            the same six tasks as Weeks 4 to 11
```

Everything works except `evaluate.py`, as long as your loop and tools
from Week 3 do.

## Run this first

```bash
python demo_evaluate.py
```

0 API calls. Three scripted runs, each checked by outcome and by
trajectory.

## The idea

An evaluation runs a fixed set of cases, checks each run, and reports
what it cost. Each run is checked two ways:

- **Outcome.** Is the final answer right?
- **Trajectory.** Did it read the right files, use the right tools, and
  stay under the tool-call limit?

A run can pass one and fail the other.

`record()` is given. It sees every tool call by swapping `tools.run` for
a version that writes each call down, then puts the real one back.

## The lab

Open `agent/evaluate.py`. `numbers_in()`, `record()`, `print_report()`
and `check_outcome()` are given. Read `check_outcome()` first: it checks
whether the run finished and whether the answer contains every expected
number, and returns one named True/False per check. Three functions are
yours:

- `check_trajectory(trace, case)`: did the run read the required files,
  use the required tools, stay under the tool-call budget, and avoid tool
  errors? Same shape as `check_outcome()`.
- `evaluate(cases, run_fn)`: run each case once with `record()`, apply
  both checks, and return one row per case.
- `benchmark(cases)`: run `evaluate()` once per strategy (loop, plan,
  orchestrate, team) on the same cases, skip any whose lab is not
  finished, and print one line per strategy: outcome, trajectory, calls,
  tokens and time.

Test it on two cases first, then all six:

```bash
python -m agent.evaluate --cases 1 3
python -m agent.evaluate
```

Add `--trace` to see every tool call each run made. Add `--strategy plan`,
`--strategy orchestrate` or `--strategy team` to evaluate your Week 4
planner, your Weeks 7-8 orchestrator or your Week 11 team instead of the
plain loop.

Once `evaluate()` works, benchmark two cases:

```bash
python -m agent.evaluate --cases 1 3 --benchmark
```

A benchmark runs the same cases with each strategy and puts the results
side by side. Your project needs the same kind of comparison: the full
system against a simpler version.

## Do not change the entry point

`python -m agent.cli --task "..."` has to keep working exactly as it does
now. The evaluation has its own entry point, `python -m agent.evaluate`,
so nothing about the agent itself changes this week.

## Watch your quota

15 requests a minute, 500 a day. An evaluation runs the agent once per
case. One full run of all six cases is about 25 to 40 calls and takes a
few minutes. `print_report()` shows what each run cost.

Use `--cases` to run one or two cases while you are writing your checks.
Run all six only once they work. A benchmark runs every case once per
strategy, so `--cases 1 3 --benchmark` costs about as much as one full
evaluation. Do not benchmark all six cases.

If something goes wrong, stop it with Ctrl+C rather than letting it run.

## Submitting

Fill in `week13-OUTPUT.md` and commit everything, including your code.

**Due 11:59pm Monday Nov 23.**
