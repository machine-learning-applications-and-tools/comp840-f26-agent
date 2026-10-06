# Week 5: Memory

COMP840 / COMP740 · ML Applications and Tools

New here? Start with the top-level `README.md` for one-time setup and
`UPDATING.md` for how to pull weekly updates. This file is this week's
instructions only.

## Pulling this week's files

Commit your own Week 4 work first. Then:

```bash
git fetch upstream
git checkout upstream/main -- README.md week05-README.md week05-OUTPUT.md .gitignore agent/cli.py agent/config.py agent/llm.py agent/memory.py demo_memory.py demo_semantic_recall.py
git add -A
git commit -m "Pull Week 5 update"
```

What each one is for:

- `week05-README.md`, `week05-OUTPUT.md`, `agent/memory.py`,
  `demo_memory.py`, `demo_semantic_recall.py` are new this week.
- `README.md` gains one line pointing to this file.
- `.gitignore` now ignores `memory/`, where your saved sessions go. Pull
  it before your first `--session` run, so you never commit session
  files by accident. If you had added your own lines to `.gitignore`,
  add them back after the pull.
- `agent/cli.py` adds `--session`.
- `agent/llm.py` and `agent/config.py` add `embed()` and `EMBED_MODEL` for
  the semantic recall demo. If you had changed `MODEL` in `config.py`,
  set it again after the pull.

Do not add `agent/loop.py`, `agent/tools.py` or `agent/planner.py` to that
list. Those are your own completed work from Weeks 3 and 4, and pulling
them would overwrite it. `tasks.py` has not changed, so leave it alone too.

If you skipped Week 4's pull, do that one first, from `week04-README.md`.
`agent/cli.py` imports your planner, so Week 5 will not run without it.

## What is here

```
agent/
    __init__.py     makes this a package
    config.py       the model name. Only place it appears.
    llm.py          generate(), with rate limiting and retries
    tools.py        the tools your agent can use
    loop.py         your Week 3 loop. Do not change it.
    planner.py      your Week 4 planner. Do not change it.
    memory.py       THE MEMORY. This is the lab.
    cli.py          command line entry point, now with --session
demo_one_turn.py    Week 3's demo, still here for reference
demo_plan_only.py, demo_react_vs_plan.py
                    Week 4's demos, still here for reference
demo_memory.py      watch memory pass between two runs, by hand
demo_semantic_recall.py   the most recent saved turn vs. the most
                          relevant one. See "Recency isn't relevance" below.
tasks.py            six tasks that need three or more tools in sequence
memory/             saved conversations land here once memory.py works
                     (gitignored, created at runtime)
```

Everything works except `memory.py`, as long as your Week 3 loop and
Week 4 planner do.

## Run this first

```bash
python demo_memory.py
```

Two API calls. It saves a fact to a JSON file, then starts a completely
separate call to `run()` and hands that file's contents back in. It does
this by hand, so you see how it works before you write `load()` and
`save()`.

## The idea

Every run so far has started from nothing. `run("My name is Karen")` and
`run("What is my name?")` are two unrelated calls unless something outside
the loop connects them.

Same trick as Week 4: fold the missing piece into the task text, and hand
that to a loop that already knows what to do with a task string. This week,
the missing piece is what happened last time. It comes from a file, not
from the model, because the model remembers nothing between calls.

## The lab

Open `agent/memory.py`. Three functions, all empty:

- `load(session)`: read a session's saved turns from disk. `[]` if there
  are none yet.
- `save(session, task, answer)`: append one turn and write the whole file
  back.
- `with_memory(task, session)`: fold prior turns into `task`, the same way
  `planner.py` folds in a plan.

Test it:

```bash
python -m agent.cli --task "My favourite language is OCaml." --session me
python -m agent.cli --task "What is my favourite language?" --session me
```

The second call should answer correctly, using nothing but what
`memory.py` wrote to disk after the first one.

## Recency isn't relevance

`with_memory()` folds in every saved turn, oldest to newest. That answers
"what happened," but not "what is this new question actually about." A
session running for weeks can easily have the relevant turn buried
somewhere in the middle, not at the end. The extension's `summarize()`
keeps only the newest turns verbatim, so that buried turn is the one it
compresses away. `demo_semantic_recall.py` shows which turn that would be,
then embeds the saved tasks and ranks them by similarity to a new question
instead of by how recent they are:

```bash
python demo_semantic_recall.py
```

Six `embed()` calls, no `generate()` calls. Not part of the required lab.
`embed()` uses `EMBED_MODEL` from `agent/config.py`, which has its own
free-tier budget: 100 requests a minute and 1,000 a day. You can see
your usage on your [AI Studio rate-limit
page](https://aistudio.google.com/rate-limit).

## Extension

Required for COMP840. Optional but encouraged for COMP740.

- **Context budgeting.** `with_memory()` folds in every saved turn, every
  time. That is Week 3's "every step resends everything" problem again,
  this time across runs instead of within one. Fill in
  `summarize(session, keep_recent=3)` at the bottom of `agent/memory.py`:
  compress everything except the most recent `keep_recent` turns into one
  summary, using one extra call to the model.

  It is not automatic. Build up at least five turns in one session, then
  call it yourself, once, from a Python shell:

  ```python
  from agent.memory import summarize
  summarize("me")
  ```

  Then answer Q5 and Q6 in `week05-OUTPUT.md`.

## Do not change the entry point

`python -m agent.cli --task "..."` has to keep working exactly as it does
now. `--session` is new and optional. In Week 12 you will run each other's
agents, and that only works if they are all invoked the same way.

## Watch your quota

15 requests a minute, 500 a day. A session used across many separate runs
resends more of its history each time. `summarize()`, the extension,
is how you cut that down.

If something goes wrong, stop it with Ctrl+C rather than letting it run.

## Submitting

Fill in `week05-OUTPUT.md` and commit everything, including your code. Do not
commit anything under `memory/`. It is gitignored on purpose.

**Due 11:59pm Monday.**
