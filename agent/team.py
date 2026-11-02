"""
Agents with different jobs.

THIS FILE IS THIS WEEK'S LAB. loop.py, delegate.py and your earlier
files do not change.

In Weeks 7-8 every worker did the same job: same instructions, same
tools, a different subtask. Here each agent has its own job:

    researcher   finds the answer in data/ and hands over JSON:
                 {"answer": ..., "source": ..., "quote": ...}
    checker      reads the cited file and decides whether it really
                 supports the answer: {"verdict": ..., "reason": ...}

Each agent is still its own loop with its own conversation. What makes
them different is their instructions and their tools. The researcher can
search, read and calculate. The checker can only read.

The handoff between them is JSON with fixed fields, so code can check
it before the next agent uses it.

Try it:

    python -m agent.cli --task "How much does the Growth plan cost per month?" --team
"""

import json
import re
import sys

from google.genai import types

from agent import llm, tools
from agent.llm import generate
from agent.loop import find_function_call

ROLE_STEPS = 6

# Each role gets only the tools its job needs.
RESEARCHER_TOOLS = ["list_files", "search_files", "read_file", "calculator"]
CHECKER_TOOLS = ["read_file"]

RESEARCHER_INSTRUCTIONS = (
    "You are the researcher. Answer the question using the files in "
    "data/. Use search_files and read_file to find the answer, and the "
    "calculator for any arithmetic. When you are done, reply with ONLY a "
    "JSON object, nothing else:\n"
    '{"answer": "your answer", '
    '"source": "the file name only, like pricing.txt", '
    '"quote": "one sentence copied exactly from that file"}'
)

CHECKER_INSTRUCTIONS = (
    "You are the checker. You get a question and another agent's answer, "
    "with the file it came from and a quote from that file. Read the "
    "source file with read_file. Decide whether the file really supports "
    "the answer to this question. Reply with ONLY a JSON object, nothing "
    "else:\n"
    '{"verdict": "ok" or "problem", "reason": "one sentence"}'
)

HANDOFF_FIELDS = ["answer", "source", "quote"]
VERDICT_FIELDS = ["verdict", "reason"]


def run_role(task, instructions, tool_names, max_steps=ROLE_STEPS,
             verbose=False):
    """
    Given, not a stub. Your Week 3 loop, with two changes:

      instructions  sent as the system instruction, so the model reads
                    them before the task on every call
      tool_names    the only tools this role is offered. If the model
                    asks for any other tool, it gets an error back
                    instead of a result.

    Returns the role's final reply as a string, like run().
    """
    schemas = [tools.TOOLS[name][1] for name in tool_names]
    config = types.GenerateContentConfig(
        system_instruction=instructions,
        tools=[types.Tool(function_declarations=schemas)],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
    )
    contents = [types.Content(role="user", parts=[types.Part(text=task)])]

    for step in range(1, max_steps + 1):
        response = generate(contents, config=config)
        call = find_function_call(response)
        if call is None:
            if verbose:
                print(f"    step {step}: answered.")
            return response.text or ""

        if verbose:
            print(f"    step {step}: {call.name}({dict(call.args)})")
        if call.name in tool_names:
            result = tools.run(call.name, dict(call.args))
        else:
            result = f"Error: {call.name} is not one of your tools."

        contents.append(response.candidates[0].content)
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_function_response(
                name=call.name, response={"result": result},
            )],
        ))

    return f"Error: gave up after {max_steps} steps without answering."


def parse_reply(text, fields):
    """
    Given. Pull a JSON object out of a reply and check it has every field.

    Finds the first {...} in the text, so a reply wrapped in ```json
    fences or with a sentence before it still works. Returns the dict, or
    None if there is no JSON, it does not parse, or a field is missing or
    is not a string. Week 2's lesson: never assume the reply is clean.
    """
    match = re.search(r"\{.*\}", text or "", re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    if any(not isinstance(data.get(f), str) for f in fields):
        return None
    return data


def _squash(text):
    """Collapse every run of spaces and line breaks into one space."""
    return " ".join(text.split())


def quote_in_file(quote, source):
    """
    Given. True if `quote` really appears in data/`source`.

    A plain string test, no model call. Line breaks and extra spaces are
    ignored, because the files wrap their lines and a model copying a
    sentence will not.
    """
    if not quote or not source:
        return False
    text = tools.read_file(source)
    if text.startswith("Error"):
        return False
    return _squash(quote) in _squash(text)


def researcher(question, feedback=None, verbose=False):
    r"""
    Run the researcher on `question` and return its handoff as a dict
    with the keys "answer", "source" and "quote".

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  Build the task. Start with the question. If `feedback` is given,
        the checker rejected an earlier answer, so add its reason:

            task = question
            if feedback:
                task += (f"\n\nA checker rejected your last answer: "
                         f"{feedback}\nLook again and fix it.")

    2.  Run the role with its own instructions and tools:

            reply = run_role(task, RESEARCHER_INSTRUCTIONS,
                             RESEARCHER_TOOLS, verbose=verbose)

    3.  Parse the handoff with parse_reply(reply, HANDOFF_FIELDS).
        If that returns None, do not crash. Return the raw reply as the
        answer, with an empty source and quote:

            {"answer": reply.strip(), "source": "", "quote": ""}

        The checker will then reject it, because an empty quote is never
        in any file.
    """
    raise NotImplementedError("write team.researcher")


def checker(question, handoff, verbose=False):
    r"""
    Check one handoff and return {"verdict": "ok" or "problem",
    "reason": "..."}.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  Check in code first. If quote_in_file(handoff["quote"],
        handoff["source"]) is False, return a problem straight away,
        with no model call:

            {"verdict": "problem",
             "reason": f"the quote is not in "
                       f"{handoff['source'] or 'any file'}"}

        Whether a quote is in a file is a string test. It does not need
        a model.

    2.  Otherwise ask the model the part code cannot answer: does the
        quote really support the answer to this question?

            task = (f"Question: {question}\n"
                    f"Answer: {handoff['answer']}\n"
                    f"Source: {handoff['source']}\n"
                    f"Quote: {handoff['quote']}")
            reply = run_role(task, CHECKER_INSTRUCTIONS, CHECKER_TOOLS,
                             verbose=verbose)

    3.  Parse it with parse_reply(reply, VERDICT_FIELDS). If that
        returns None, or the verdict is not "ok" or "problem", return a
        problem. A checker that cannot read its own reply must not pass
        the answer.

            {"verdict": "problem",
             "reason": "the checker's reply did not parse"}

    4.  Otherwise return the parsed verdict.
    """
    raise NotImplementedError("write team.checker")


def team(task, max_steps=ROLE_STEPS, verbose=True):
    """
    Researcher, then checker, then one retry if the checker found a
    problem. Returns the final answer as a string.

    Takes the same arguments as run(), so the command line can call it
    the same way. max_steps is accepted for that reason and not used.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  handoff = researcher(task). If verbose, print it.

    2.  verdict = checker(task, handoff). If verbose, print it.

    3.  If verdict["verdict"] is not "ok", try once more. Pass the
        checker's reason back, and nothing else:

            handoff = researcher(task, feedback=verdict["reason"])
            verdict = checker(task, handoff)

        One retry only. Without a cap, two agents that disagree can
        spend your whole quota.

    4.  Build the answer string: handoff["answer"], then the source and
        quote if there is a source. If the final verdict is still not
        "ok", add a line saying the checker was not satisfied, and why.
        Never hide a failed check from the user.
    """
    raise NotImplementedError("write team.team")


# =======================================================================
# EXTENSION. Required for everyone.
#
# A checker that approves everything looks fine when you run the team.
# The only way to know it works is to test it on its own, with answers
# you already know are right or wrong.
# =======================================================================

def test_checker(cases):
    """
    Run checker() on every case in checker_cases.py and report how it
    did.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    Each case has "question", "handoff" and "expected" ("ok" or
    "problem").

    1.  For each case, call checker(case["question"], case["handoff"]).
        Count the calls it made: copy llm.stats["calls"] before and
        subtract after.

    2.  Print one line per case: expected, got, right or wrong, calls,
        and the checker's reason.

    3.  Count and print two numbers:
            planted errors caught    "problem" cases it called "problem"
            false alarms             "ok" cases it called "problem"

    4.  Return the counts as a dict.

    Run it with:  python -m agent.team --test-checker
    """
    raise NotImplementedError("write team.test_checker")


# =======================================================================
# GRADUATE EXTENSION. COMP840 required, COMP740 optional.
#
# Your project's evaluation needs cost and reliability per agent, not
# just for the whole team.
# =======================================================================

REPORT_QUESTIONS = [
    "How much does the Growth plan cost per month?",
    "Is SSO available on the Starter plan?",
    "Are duplicate charges refunded, and is any discretion needed?",
    "How long do email/password sessions last by default?",
]


def team_report(questions):
    """
    For each question, run the researcher and then the checker, and
    report each agent separately.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    Measure each agent the same way as Weeks 7-8's compare():

        before = dict(llm.stats)
        handoff = researcher(q)
        calls = llm.stats["calls"] - before["calls"]
        tokens = llm.stats["input_tokens"] - before["input_tokens"]

    1.  For each question, record for the researcher: calls, input
        tokens, whether the handoff parsed (it has a source), and
        whether its quote is really in the file (quote_in_file).

    2.  Record for the checker: calls, input tokens, and its verdict.

    3.  Print one block per question, then the totals: how many
        handoffs parsed, how many quotes were real, and the total calls
        and input tokens for each agent.

    Run it with:  python -m agent.team --report
    """
    raise NotImplementedError("write team.team_report")


if __name__ == "__main__":
    if "--test-checker" in sys.argv:
        from checker_cases import CASES
        test_checker(CASES)
    elif "--report" in sys.argv:
        team_report(REPORT_QUESTIONS)
    else:
        print(team(REPORT_QUESTIONS[0]))
    llm.report()
