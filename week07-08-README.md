# Weeks 7-8: Sandboxing and sub-agents

COMP840 / COMP740 · ML Applications and Tools

One lab across two classes: Tuesday Oct 13 and Wednesday Oct 14. One pull,
one `week07-08-OUTPUT.md`, one deadline.

New here? Start with the top-level `README.md` for one-time setup and
`UPDATING.md` for how to pull weekly updates. This file is this lab's
instructions only.

## Pulling this lab's files

Commit your own Week 6 work first. Then, once, before Tuesday's class:

```bash
git fetch upstream
git checkout upstream/main -- README.md week07-08-README.md week07-08-OUTPUT.md agent/cli.py agent/sandbox.py agent/delegate.py demo_sandbox.py demo_subagent.py
git add -A
git commit -m "Pull Weeks 7-8 update"
```

What each one is for:

- `agent/sandbox.py` and `demo_sandbox.py` are Tuesday's lab and demo.
- `agent/delegate.py` and `demo_subagent.py` are Wednesday's lab and demo.
- `week07-08-README.md` and `week07-08-OUTPUT.md` are new.
- `README.md` gains one line pointing to this file.
- `agent/cli.py` adds `--orchestrate`, and loads `sandbox.py` so the agent
  can use `run_python`.

Do not add `agent/tools.py`, `agent/loop.py`, `agent/planner.py`,
`agent/memory.py`, or `agent/retrieval.py` to that list. They hold your own
work from earlier weeks, including the classifier you added to `tools.py`
in Week 3. This lab does not change any of them.

If you skipped the Week 6 pull, do that one first. `agent/cli.py` imports
`retrieval.py`.

## What is here

```
agent/
    tools.py        your tools from Week 3. Not touched this lab.
    sandbox.py      run_python. TUESDAY'S LAB.
    delegate.py     sub-agents. WEDNESDAY'S LAB.
    cli.py          command line entry point, now with --orchestrate
    loop.py, planner.py, memory.py, retrieval.py   your earlier weeks
demo_sandbox.py     what "sandboxed" actually buys you. 0 API calls.
demo_subagent.py    one agent vs. two workers on the same task
```

## Tuesday: a tool that can go wrong

### The idea

Every capability so far has been information: a plan, prior turns,
retrieved documents, all folded into the task string before `run()` sees
them. `run_python()` is different. It runs code the model just wrote, and
that code can do anything your user account can do unless you stop it.
You cannot make it safe by checking its text, the way `calculator()`
does. Safety has to come from where it runs.

### Run this first

```bash
python demo_sandbox.py
```

0 API calls. Watch a naive `exec()` tool leak a fake secret, watch a plain
subprocess leak it too, and watch a stripped environment stop it. It pauses after
part 2. Press Enter to see part 3.

### The lab

Open `agent/sandbox.py`. Two functions, both required:

- `run_python(code)`: run `code` as a **separate process** with
  `subprocess.run([sys.executable, "-c", code], ...)`, not `exec()` in
  this one, with a timeout, and return what it printed.
- `run_python_contained(code)`: the same, plus `env=_minimal_env()`
  (given: `{}` on Mac, only `SYSTEMROOT` on Windows so Python can start),
  so the child cannot see your environment variables.

Why a separate process: when the time runs out, the operating system kills
the child process. Code stuck in `while True: pass` inside this process
could not be stopped that way.

Why both: `run_python()` stops a hang. `run_python_contained()` also hides
the environment, including your API key. Neither makes running code fully
safe. The code can still read or delete your files and use the network.
Say so honestly in `week07-08-OUTPUT.md` rather than claiming "sandboxed."

Check both without the agent:

```bash
python -m agent.sandbox
```

The last lines of `sandbox.py` add `run_python` to the same tool registry
your Week 3 tools live in. `loop.py` does not change.

Test it:

```bash
python -m agent.cli --task "Use Python to compute the 15th Fibonacci number."
```

The model has to choose to call `run_python` itself. If it answers without
it, try a task that is more obviously code-shaped.

## Wednesday: sub-agents

### The idea

So far one agent does everything, in one conversation. Every tool result
it reads stays in that conversation and is sent again on every step. A
long task fills the context with detail the agent no longer needs.

A sub-agent is another call to `run()`, with its own fresh conversation.
It does one piece of the work and hands back only its final answer. That
is context isolation, and you already have it: `run()` starts a new
conversation every time it is called.

### Run this first

```bash
python demo_subagent.py
```

About 10 to 15 API calls. The same task done by one agent, then split by
hand across two workers. Compare the prompt sizes, and the total calls.

### The lab

Open `agent/delegate.py`. `split_task()` is given. Two functions are not:

- `run_worker(subtask)`: run one sub-agent and return only its answer.
- `orchestrate(task)`: split the task, run one worker per subtask, and
  combine their answers with one more model call.

`MAX_WORKERS` caps how many workers one task can start. Workers are plain
`run()` calls, so they cannot start workers of their own.

Test it:

```bash
python -m agent.cli --task "$(python -c 'from tasks import TASKS; print(TASKS[0])')" --orchestrate
```

This is also a starting point for your project if you are building a
multi-agent system.

## Extension

Required for COMP840. Optional but encouraged for COMP740.

- **Is the split worth it?** Fill in `compare(task)` at the bottom of
  `agent/delegate.py`. Run the same task with one agent and orchestrated,
  and print calls and input tokens for each part: the single agent, the
  split, each worker, and the combine step. This is the per-agent
  measurement your project's evaluation needs.

## Do not change the entry point

`python -m agent.cli --task "..."` has to keep working exactly as it does
now. `--orchestrate` is new and optional.

## Watch your quota

15 requests a minute, 500 a day. `sandbox.py` costs no API calls. Sub-agents
multiply calls: a split, one run per worker, and a combine. Running workers
at the same time would not help, because the limit is per minute.

If something goes wrong, stop it with Ctrl+C rather than letting it run.

## Submitting

Fill in `week07-08-OUTPUT.md` and commit everything, including your code.
One submission for both classes.

**Due 11:59pm Monday Oct 19.**
