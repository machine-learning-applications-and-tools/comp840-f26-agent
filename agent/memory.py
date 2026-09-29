"""
Memory across runs.

THIS FILE IS THE LAB. Everything else already works, including loop.py --
you are not changing it, same as last week.

Every run so far has started from nothing. Tell it your name in one run,
ask for it back in the next, and it has no idea -- not because the model
forgot, but because nothing saved the first run's turn anywhere.

Same trick as Week 4's planner: fold the missing piece into the task
text, and hand that to a loop that already knows what to do with a task
string. This week, the missing piece is what happened last time.
"""

import json
from pathlib import Path

MEMORY_DIR = (Path(__file__).parent.parent / "memory").resolve()


def _path(session: str) -> Path:
    MEMORY_DIR.mkdir(exist_ok=True)
    return MEMORY_DIR / f"{session}.json"


def load(session: str) -> list[dict]:
    """
    Load the saved turns for `session`, oldest first.

    Returns a list of {"task": ..., "answer": ...} dicts, or [] if this
    session has never been saved before.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  If _path(session) does not exist, return []. A new session is
        not an error.

    2.  Otherwise read the file and json.loads() it. It is exactly the
        list save() wrote below -- no reshaping needed on the way back
        in.
    """
    raise NotImplementedError("write memory.load")


def save(session: str, task: str, answer: str) -> None:
    """
    Append one (task, answer) turn to `session`'s saved history.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  Load what is already there: turns = load(session).

    2.  Append {"task": task, "answer": answer} to it.

    3.  Write the whole list back to _path(session) as JSON. You are
        overwriting the file with the whole list every time, not
        appending text to it. Two JSON objects written back to back
        are not a list of two objects, and json.loads() will reject
        the file.
    """
    raise NotImplementedError("write memory.save")


def with_memory(task: str, session: str) -> str:
    """
    Fold this session's prior turns into task, the same way Week 4 folded
    a plan in. What comes back is just a task string -- hand it to run()
    or run_with_plan() exactly as you would the original task.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  turns = load(session). If there are none, return task unchanged
        -- nothing to fold in yet.

    2.  Build a block describing prior turns, oldest first:

            "\\n".join(
                f"You: {t['task']}\\nYou answered: {t['answer']}"
                for t in turns
            )

    3.  Return task with that block prepended, clearly labelled as prior
        conversation rather than part of the current request:

            f"Earlier in this conversation:\\n{block}\\n\\nNow: {task}"

    Saving is NOT this function's job. Call memory.save() yourself, after
    you have the answer, with the ORIGINAL task -- not the folded one --
    so next time's block does not nest a conversation inside a
    conversation.
    """
    raise NotImplementedError("write memory.with_memory")


# =======================================================================
# GRADUATE EXTENSION -- COMP840 required, COMP740 optional
#
# with_memory() folds in EVERY saved turn, forever. A session used every
# day for a month resends a month of history on every single call. That
# is Week 3's "every step resends everything" slide, back again -- this
# time across runs instead of within one.
# =======================================================================

def summarize(session: str, keep_recent: int = 3) -> None:
    """
    Compress everything except the most recent `keep_recent` turns into
    one short summary, and rewrite the session's saved history to be
    just that summary followed by the recent turns, unchanged.

    Not automatic -- call this yourself, occasionally, from a Python
    shell. A real system might call it every N turns; showing it works
    once is enough for this lab.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  turns = load(session). If there are keep_recent or fewer,
        return without changing anything -- nothing to compress yet.

    2.  Split into older = turns[:-keep_recent] and
        recent = turns[-keep_recent:].

    3.  Ask the model to summarize older in a few sentences. One call,
        no tools attached:

            from agent.llm import generate

            block = "\\n".join(
                f"You: {t['task']}\\nYou answered: {t['answer']}"
                for t in older
            )
            response = generate(
                "Summarize this conversation history in 2-3 sentences, "
                "keeping only what would matter for future questions.\\n\\n"
                f"{block}"
            )

    4.  Rewrite the session's saved history as one summary turn followed
        by `recent`, unchanged:

            new_turns = [
                {"task": "(earlier conversation)", "answer": response.text},
            ] + recent
            _path(session).write_text(json.dumps(new_turns))
    """
    raise NotImplementedError("write memory.summarize")
