"""
Sub-agents.

THIS FILE IS PART OF THIS WEEK'S LAB (Wednesday). The other part is
sandbox.py (Tuesday). loop.py already works, and you are not changing it.

So far one agent has done everything, in one conversation. Every tool
result it reads stays in that conversation for the rest of the task, and
gets sent again on every step. A long task fills the context with detail
the agent no longer needs.

A sub-agent fixes that. It is another call to run(), with its own fresh
conversation. It does its piece of work, and hands back only its final
answer. The caller never sees the worker's tool calls, only the one
line it returns. That is context isolation, and you get it for free:
run() already starts a new conversation every time it is called.

This week's pattern is the simplest one: the CODE orchestrates.

    1. split    one model call turns the task into a few subtasks
    2. work     one worker per subtask, each a fresh run()
    3. combine  one model call turns the workers' answers into one answer

Try it:

    python -m agent.cli --task "..." --orchestrate
"""

import json

from agent.llm import generate
from agent.loop import run

# Guardrails. Every multi-agent system needs a cap, or one bad split can
# spend a day of quota. Workers are plain run() calls, so they cannot
# spawn workers of their own.
MAX_WORKERS = 4
WORKER_STEPS = 6


def split_task(task: str) -> list[str]:
    """
    Given, not a stub. Ask the model to break `task` into independent
    subtasks, as a JSON list of strings.

    Same prompted-JSON pattern as Week 2, with Week 2's lesson built in:
    if the reply does not parse, do not crash. Fall back to treating the
    whole task as a single subtask.
    """
    response = generate(
        "Split this task into at most "
        f"{MAX_WORKERS} independent subtasks that could each be done "
        "separately by someone who has not seen the others. Each subtask "
        "must make sense on its own. Reply with ONLY a JSON list of "
        "strings, nothing else.\n\n"
        f"Task: {task}"
    )
    text = response.text.strip().removeprefix("```json").strip("`").strip()
    try:
        subtasks = json.loads(text)
    except json.JSONDecodeError:
        return [task]
    if not isinstance(subtasks, list) or not subtasks:
        return [task]
    return [str(s) for s in subtasks][:MAX_WORKERS]


def run_worker(subtask: str, verbose: bool = False) -> str:
    """
    Run one sub-agent on `subtask` and return only its final answer.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  Call run() on the subtask, with max_steps=WORKER_STEPS, passing
        `verbose` straight through:

            answer = run(subtask, max_steps=WORKER_STEPS, verbose=verbose)

        run() builds a brand new conversation containing nothing but
        `subtask`. The worker cannot see the original task, the other
        subtasks, or anything the other workers found. That is the
        isolation. Notice you did not have to write anything to get it.

    2.  Return the answer. Only the answer: not the worker's tool calls,
        not its steps. Whoever called the worker sees this one string.
    """
    raise NotImplementedError("write delegate.run_worker")


def orchestrate(task: str, max_steps: int = WORKER_STEPS,
                verbose: bool = True) -> str:
    """
    Split `task`, give each piece to a worker, combine their answers.

    Takes the same arguments as run(), so the command line can call it
    the same way. max_steps is accepted for that reason and not used:
    each worker gets WORKER_STEPS.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  Split the task. split_task() is given and already caps the list
        at MAX_WORKERS:

            subtasks = split_task(task)

        If verbose, print the subtasks, numbered. You cannot judge a
        split you never see.

    2.  Run one worker per subtask, in order, and keep each answer:

            answers = [run_worker(s) for s in subtasks]

        If verbose, print each worker's answer as it comes back.

    3.  Combine. One more model call, no tools, that sees the original
        task and every worker's question and answer, and nothing else:

            block = "\n\n".join(
                f"Worker {i} was asked: {s}\nWorker {i} answered: {a}"
                for i, (s, a) in enumerate(zip(subtasks, answers), 1)
            )
            response = generate(
                f"Task: {task}\n\n"
                f"Several workers each handled one part of this task:\n\n"
                f"{block}\n\n"
                "Combine their answers into one answer to the task. If "
                "they disagree or something is missing, say so."
            )
            return response.text

    Give the combine step only the workers' answers, not their full
    conversations. That is what keeps each worker's context separate.
    """
    raise NotImplementedError("write delegate.orchestrate")


# =======================================================================
# GRADUATE EXTENSION. COMP840 required, COMP740 optional.
#
# Is the split worth it? Run the same task both ways and find out where
# the calls and tokens actually went, agent by agent.
# =======================================================================

def compare(task: str) -> None:
    """
    Run `task` once with a single agent (run()) and once orchestrated,
    and print each answer plus a cost breakdown.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    llm.stats counts calls and tokens for the whole script run. Take a
    copy before and after each thing you want to measure, and subtract,
    the same way Week 4's compare() did:

        from agent import llm
        before = dict(llm.stats)
        ...
        used = llm.stats["calls"] - before["calls"]

    1.  Single agent: run(task) on its own. Record its answer, calls,
        and input tokens.

    2.  Orchestrated: do the three steps of orchestrate() yourself here,
        so you can measure each part separately. Record calls and input
        tokens for: the split, EACH worker, and the combine step.

    3.  Print both answers, then one cost line per part, for example:

            single agent      9 calls    14,200 input tokens
            split             1 call        310 input tokens
            worker 1          3 calls     2,900 input tokens
            ...
            combine           1 call        880 input tokens

    Answer in week07-08-OUTPUT.md: which version cost more, and where did the
    orchestrated version's tokens go? Compare the combine step's input
    tokens with the single agent's. What does that number say about
    context isolation?
    """
    raise NotImplementedError("write delegate.compare")
