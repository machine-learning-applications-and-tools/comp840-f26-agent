# Week 11: Agents with different jobs

COMP840 / COMP740 · ML Applications and Tools

New here? Start with the top-level `README.md` for one-time setup and
`UPDATING.md` for how to pull weekly updates. This file is this week's
instructions only.

## Pulling this week's files

Commit your own Weeks 7-8 work first. Then:

```bash
git fetch upstream
git checkout upstream/main -- README.md week11-README.md week11-OUTPUT.md agent/cli.py agent/team.py checker_cases.py demo_roles.py demo_handoff.py
git add -A
git commit -m "Pull Week 11 update"
```

What each one is for:

- `agent/team.py` is this week's lab.
- `checker_cases.py` holds the test cases for the extension.
- `demo_roles.py` and `demo_handoff.py` are this week's demos.
- `week11-README.md` and `week11-OUTPUT.md` are new.
- `README.md` gains one line pointing to this file.
- `agent/cli.py` adds `--team`.

Do not add `agent/tools.py`, `agent/loop.py`, `agent/planner.py`,
`agent/memory.py`, `agent/retrieval.py`, `agent/sandbox.py` or
`agent/delegate.py` to that list. They hold your own work from earlier
weeks. This lab does not change any of them.

If you skipped the Weeks 7-8 pull, do that one first. `agent/cli.py`
imports `delegate.py`.

## What is here

```
agent/
    team.py         a researcher and a checker. THIS WEEK'S LAB.
    cli.py          command line entry point, now with --team
    loop.py, tools.py, planner.py, memory.py, retrieval.py,
    sandbox.py, delegate.py      your earlier weeks
checker_cases.py    six handoffs for testing the checker on its own
demo_handoff.py     what a handoff has to survive. 0 API calls.
demo_roles.py       two agents, two jobs. About 6 to 10 API calls.
```

## Run these first

```bash
python demo_handoff.py
python demo_roles.py
```

`demo_handoff.py` costs nothing. It runs five model-style replies through
`parse_reply()` and three quotes through `quote_in_file()`.
`demo_roles.py` runs the researcher on one question, then the checker on
two handoffs, one with a wrong number planted in it.

## The idea

In Weeks 7-8 every worker did the same job, with a different subtask. In
your project, each agent has a different job. What makes the jobs
different is two things you give each agent:

- **Instructions.** What this agent is for, and what it must hand back.
- **Tools.** Only the tools its job needs. The researcher can search,
  read and calculate. The checker can only read.

The agents pass work to each other as JSON with fixed fields. That is the
**handoff**. Code checks it before the next agent uses it.

Some checks do not need a model at all. Whether a quote is really in a
file is a string test. Whether that quote answers the question is a
judgement. The checker does the first in code and asks the model only for
the second.

## The lab

Open `agent/team.py`. `run_role()`, `parse_reply()` and
`quote_in_file()` are given. Three functions are not:

- `researcher(question, feedback=None)`: run the researcher role and
  return its handoff as a dict. If the reply does not parse, return the
  raw reply with an empty source and quote.
- `checker(question, handoff)`: check the quote in code first. If it is
  real, ask the model whether it supports the answer. If the model's reply
  does not parse, or the verdict is not ok or problem, return a problem.
- `team(task)`: researcher, then checker, then one retry with the
  checker's reason if it found a problem.

Test it:

```bash
python -m agent.cli --task "How much does the Growth plan cost per month?" --team
```

## Extension

Required for everyone.

- **Test the checker on its own.** Fill in `test_checker(cases)` at the
  bottom of `agent/team.py`. It runs `checker()` on the six cases in
  `checker_cases.py`, three right and three with a planted error, and
  reports how many errors it caught and how many false alarms it raised.

  ```bash
  python -m agent.team --test-checker
  ```

## Graduate extension

Required for COMP840. Optional but encouraged for COMP740.

- **Report each agent separately.** Fill in `team_report(questions)`.
  For each question, record the researcher's calls and input tokens,
  whether its handoff parsed, and whether its quote was real, then the
  checker's calls, tokens and verdict. Print totals per agent.

  ```bash
  python -m agent.team --report
  ```

## Do not change the entry point

`python -m agent.cli --task "..."` has to keep working exactly as it does
now. `--team` is new and optional.

## Watch your quota

15 requests a minute, 500 a day. One `--team` run is about 4 to 8 calls,
and up to twice that if the checker asks for a retry. `--test-checker` is
about 10 calls. One of the six cases costs nothing, because the code
check catches it. `--report` is about 25 calls.

If something goes wrong, stop it with Ctrl+C rather than letting it run.

## Submitting

Fill in `week11-OUTPUT.md` and commit everything, including your code.

**Due 11:59pm Monday Nov 9.**
