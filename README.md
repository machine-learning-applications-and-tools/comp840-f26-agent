# Week 3 — The harness

COMP840 / COMP740 · ML Applications and Tools

**This repository is yours for the rest of the term.** Weeks 3 to 12 all build
on it. Do not start a new one each week.

## Setup

```bash
python3 -m venv .venv          # Windows: python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Copy your `.env` across from Week 2, or create one containing:

```
GEMINI_API_KEY=your-key-here
```

## What is here

```
agent/
    __init__.py     makes this a package
    config.py       the model name. Only place it appears.
    llm.py          generate(), with rate limiting and retries
    tools.py        the tools your agent can use
    loop.py         THE LOOP. This is the lab.
    cli.py          command line entry point
demo_one_turn.py    watch one turn happen, step by step
```

Everything works except `loop.py`.

## Run this first

```bash
python demo_one_turn.py
```

Two API calls. It walks through a single turn of the loop with each step
labelled, so you can see what you are about to build.

## The lab

### 1. Write the loop

Open `agent/loop.py`. The `run()` function is empty and its docstring tells
you, in order, what the body has to do.

It is about fifteen lines. Test it with:

```bash
python -m agent.cli --task "What is 17 times 23, plus 100?"
```

That task needs the calculator, so if it comes back with 491 and you can see
a tool call in the output, your loop works.

### 2. Add your classifier as a second tool

Open `agent/tools.py`. There is a worked example, `calculator`, showing the
shape: a Python function, a schema, and an entry in `TOOLS`.

Port your Week 2 classifier in the same way. Then check the agent can use it:

```bash
python -m agent.cli --task "Classify this ticket: I was charged twice."
```

### 3. Answer the questions

In `OUTPUT.md`.

## Extension

Required for COMP840. Optional but encouraged for COMP740.

- **Step limit.** What happens when `max_steps` runs out? Make the difference
  between "finished" and "gave up" visible to whoever called it.
- **Tool failure.** Make the calculator fail on purpose, by asking for
  something with letters in it. Does your loop crash, or does the model get
  told and recover? Which do you think is better, and why?

## Do not change the entry point

`python -m agent.cli --task "..."` has to keep working exactly as it does now.
In Week 12 you will run each other's agents, and that only works if they are
all invoked the same way. Add options if you want. Do not remove `--task`.

## Watch your quota

15 requests a minute, 500 a day. Each run of your loop is several calls, and
a loop with a bug can be many more. `MAX_STEPS` exists partly to protect you
from yourself.

If something goes wrong, stop it with Ctrl+C rather than letting it run.

## Submitting

Fill in `OUTPUT.md` and commit everything, including your code.

**Due 11:59pm Sunday.** Reference solution goes up Monday morning.
