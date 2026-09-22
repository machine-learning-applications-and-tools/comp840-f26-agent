"""
The planner.

THIS FILE IS THE LAB. loop.py already works and you are not changing it.

Week 3's loop reacts one step at a time: call the model, see if it wants
a tool, run the tool, repeat. That works, but the model never has more
than the immediate next step in view -- it cannot notice a multi-step
task needs three tools in a particular order before it has already
started.

This week, the model plans before it acts. One extra call, up front, with
no tools attached: "here is the task, write a numbered plan before you do
anything." Then last week's loop runs exactly as it already does, except
the plan is sitting in the conversation the whole time, so every
tool-choosing step downstream can see it and follow it.
"""

from google.genai import types

from agent import llm
from agent.llm import generate
from agent.loop import MAX_STEPS, run


def make_plan(task: str) -> list[str]:
    """
    Ask the model for a numbered plan, before any tool runs.

    Args:
        task: what the user wants, in plain language -- the same string
              you would otherwise hand straight to loop.run().

    Returns:
        The plan as a list of strings, one step per entry, in the order
        the model wrote them. Not the whole reply as one blob -- actually
        split into steps, so run_with_plan() below can hand the loop a
        clean numbered list rather than whatever prose came back.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  Call the model with NO tools attached. Without a tools config,
        the reply is always text -- there is nothing to hand back to
        find_function_call(), and you do not need it here.

            response = generate([
                types.Content(role="user", parts=[types.Part(text=(
                    "Before doing anything, write a short numbered plan "
                    "for this task. One short step per line, no more "
                    "than five steps, plain language, no code.\\n\\n"
                    f"Task: {task}"
                ))]),
            ])

    2.  Split response.text into a list of steps. The model will not
        format this identically every time -- decide what "one step per
        line" means when the numbering comes back as "1.", "1)", a bare
        "-", or something else, and handle at least the common cases.

    3.  Return the list. If nothing in the reply looks like a numbered
        step, return the whole reply as a single-item list rather than
        raising. A bad plan should degrade the run, not crash it before
        it starts.
    """
    raise NotImplementedError("write the planner")


def run_with_plan(task: str, max_steps: int = MAX_STEPS, verbose: bool = True) -> str:
    """
    Plan, then execute. The only new idea this week -- everything after
    the plan exists is loop.run(), unchanged.

    Args:
        task:       what the user wants, in plain language
        max_steps:  passed straight through to run()
        verbose:    passed straight through to run(), and used here too

    Returns:
        Whatever run() returns. This function does not introduce a new
        kind of result; it only changes what run() is told to work from.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  Get a plan.
            steps = make_plan(task)

    2.  If verbose, print it. You cannot evaluate a plan you never see,
        and a bad plan is a different failure than a bad loop -- if the
        run goes wrong, you need to be able to tell which one broke.

    3.  Build one task string that carries the plan alongside the
        original request, and hand THAT to run() -- do not step through
        the plan yourself, and do not touch loop.py to make this work:

            numbered = "\\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
            annotated_task = (
                f"{task}\\n\\nYou already wrote this plan for yourself:\\n"
                f"{numbered}\\n\\nFollow it, using tools as needed."
            )
            return run(annotated_task, max_steps=max_steps, verbose=verbose)

    That line is the whole point of the week: last week's loop did not
    need to change at all to make use of a plan it never knows exists.
    """
    raise NotImplementedError("write the planner")


# =======================================================================
# COMPARE -- given, not a stub. This week's focus is make_plan() and
# run_with_plan() above; this function just measures what they did, so
# it is handed to you rather than adding a third thing to write.
#
# Required for everyone: run this against all six tasks in tasks.py, and
# write up three of them in week04-OUTPUT.md -- one where planning won, one
# near-tie, one where reactive won. Planning costs an extra call before
# the loop even starts. Does it pay for itself, or is it ceremony? The
# answer is different for different tasks -- that is the finding.
# =======================================================================

def compare(task: str, max_steps: int = MAX_STEPS) -> None:
    """
    Run the same task both ways -- reactive (run()) and planned
    (run_with_plan()) -- and print both answers and their cost.

    Nothing structured to return here. This is meant to be read while it
    runs, not parsed afterward.
    """
    print(f"\ntask: {task}\n")

    # llm.stats accumulates for the whole script run, not per call, so
    # snapshot it before each run and diff afterward.
    print("-- reactive (run) --")
    before = dict(llm.stats)
    answer_a = run(task, max_steps=max_steps)
    after_a = dict(llm.stats)
    calls_a = after_a["calls"] - before["calls"]
    tokens_a = after_a["output_tokens"] - before["output_tokens"]
    print(f"\nanswer: {answer_a}")
    print(f"cost:   {calls_a} calls, {tokens_a} output tokens")

    print("\n-- planned (run_with_plan) --")
    before = dict(llm.stats)
    answer_b = run_with_plan(task, max_steps=max_steps)
    after_b = dict(llm.stats)
    calls_b = after_b["calls"] - before["calls"]
    tokens_b = after_b["output_tokens"] - before["output_tokens"]
    print(f"\nanswer: {answer_b}")
    print(f"cost:   {calls_b} calls, {tokens_b} output tokens")

    print(f"\nplanning cost {calls_b - calls_a:+d} calls "
          f"and {tokens_b - tokens_a:+d} output tokens versus reactive.")


# =======================================================================
# GRADUATE EXTENSION -- COMP840 required, COMP740 optional.
# =======================================================================

def reflect(task: str, max_steps: int = MAX_STEPS, verbose: bool = True) -> str:
    """
    Run once, ask the model to critique its own answer, and retry once
    if the critique finds a real problem.

    Args:
        task:       what the user wants, in plain language
        max_steps:  passed straight through to run_with_plan(), both times
        verbose:    passed straight through, and used here too

    Returns:
        The second answer if a retry happened, otherwise the first one.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  Get a first answer, same as any other week:

            answer = run_with_plan(task, max_steps=max_steps, verbose=verbose)

    2.  Ask for a critique. One more call, no tools attached -- same shape
        as make_plan(), asking a different question:

            response = generate([
                types.Content(role="user", parts=[types.Part(text=(
                    "Here is a task and an answer someone gave for it. "
                    "Does the answer actually satisfy the task? If it is "
                    "fine, reply with exactly: OK. If something is wrong "
                    "or incomplete, say what, in one short paragraph.\\n\\n"
                    f"Task: {task}\\n\\nAnswer: {answer}"
                ))]),
            ])
            critique = response.text.strip()

    3.  Decide whether to retry. A critique is exactly as unpredictable in
        format as a plan is -- do not require an exact match. Treating
        anything that is not a short "OK"-shaped reply as "found a
        problem" is a reasonable, simple rule; degrade toward keeping the
        first answer if you are unsure, the same instinct as make_plan().

    4.  If the critique found a problem, retry once -- fold it into the
        task text, the same trick as run_with_plan() itself:

            annotated_task = (
                f"{task}\\n\\nA first attempt at this got this feedback:\\n"
                f"{critique}\\n\\nTry again, taking it into account."
            )
            return run_with_plan(annotated_task, max_steps=max_steps, verbose=verbose)

        Otherwise, just return the first answer. Cap this at ONE retry --
        do not loop until the critique is happy, that is a quota problem
        waiting to happen, not this week's lesson.
    """
    raise NotImplementedError("write the reflection")
