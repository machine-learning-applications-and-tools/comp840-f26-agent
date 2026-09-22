"""
Week 4 demo · Same task, two strategies, back to back

Runs one task two different ways: reactively (last week's loop, no plan
at all) and plan-then-execute (the exact fold run_with_plan() will do,
built by hand here since planner.py is not written yet at this point in
class -- same reason demo_plan_only.py never imports agent.planner).

Run:  python demo_react_vs_plan.py
Costs at least 3 API calls (1 plan call + at least 1 step each way).

Both runs below get a higher step ceiling than the lab's own MAX_STEPS --
this is a live demo, not the lab, and a demo that hits loop.py's default
10-step cap without answering makes for a bad class moment. This does not
change loop.py or MAX_STEPS itself, only what this one script asks for.

Both runs also use run_with_trace() below instead of agent.loop.run()
directly. It is the same loop, step for step -- same config, same
stopping condition, same tools -- copied here only so a multi-line
search_files() result prints on separate lines instead of as one long
line with literal \\n's in it. agent.loop.run() itself is untouched, and
is still what planner.py and everything else in the lab actually calls.
"""

from google.genai import types

from agent import llm, tools
from agent.llm import generate, report
from agent.loop import find_function_call
from tasks import TASKS

LINE = "-" * 66
TASK = TASKS[0]
DEMO_MAX_STEPS = 20  # headroom for this live demo only -- see note above


def run_with_trace(task: str, max_steps: int) -> str:
    """
    agent.loop.run(), copied here so this demo can print a multi-line tool
    result across several lines. Everything except that one print is
    identical to run() -- same config, same stopping condition, same
    tools -- so the calls this makes, and their cost, match run() exactly.
    """
    config = types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=tools.schemas())],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
    )
    contents = [types.Content(role="user", parts=[types.Part(text=task)])]

    for step in range(1, max_steps + 1):
        response = generate(contents, config=config)
        call = find_function_call(response)

        if call is None:
            print(f"  step {step}: answered.")
            return response.text

        print(f"  step {step}: {call.name}({dict(call.args)})")
        result = tools.run(call.name, dict(call.args))

        if "\n" in result:
            print("    ->")
            for line in result.splitlines():
                print(f"       {line}")
        else:
            print(f"    -> {result!r}")

        contents.append(response.candidates[0].content)
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_function_response(
                name=call.name,
                response={"result": result},
            )],
        ))

    print(f"  gave up after {max_steps} steps.")
    return f"Error: gave up after {max_steps} steps without answering."


print(LINE)
print("Strategy 1: ReAct -- decide one step at a time, no plan\n")
print(f'  task: "{TASK}"')

before = dict(llm.stats)
answer_reactive = run_with_trace(TASK, DEMO_MAX_STEPS)
after_reactive = dict(llm.stats)
calls_reactive = after_reactive["calls"] - before["calls"]

print(f"\n  answer: {answer_reactive}")
print(f"  cost:   {calls_reactive} calls")

print("\n" + LINE)
print("Strategy 2: plan-then-execute -- write the plan first, then run it\n")

before = dict(llm.stats)
plan_response = generate(
    "Before doing anything, write a short numbered plan for this task. "
    "One short step per line, no more than five steps, plain language, "
    "no code.\n\n"
    f"Task: {TASK}"
)
plan_text = plan_response.text.strip()
print("  plan:")
print("  " + plan_text.replace("\n", "\n  "))

annotated_task = (
    f"{TASK}\n\n"
    f"You already wrote this plan for yourself:\n{plan_text}\n\n"
    "Follow it, using tools as needed."
)
answer_planned = run_with_trace(annotated_task, DEMO_MAX_STEPS)
after_planned = dict(llm.stats)
calls_planned = after_planned["calls"] - before["calls"]

print(f"\n  answer: {answer_planned}")
print(f"  cost:   {calls_planned} calls (includes the plan call)")

print("\n" + LINE)
print(f"""
Same task, same tools, same model. {calls_reactive} calls reactive versus
{calls_planned} calls planned -- the gap between them is exactly what this
week's compare() extension asks you to measure yourself, on tasks you pick.

Neither strategy is "correct." ReAct adapts the moment a tool result
changes what is needed, and costs nothing extra up front. Plan-then-
execute commits to an order before spending a single tool call, and gives
you something to read and sanity-check before it runs -- but that plan
can go stale the instant step 1's result changes what step 3 should have
been.
""")

report()
