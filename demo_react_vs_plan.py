"""
Week 4 demo · Same task, two strategies, back to back

Runs one task two ways: reactively (last week's loop, no plan) and
plan-then-execute (the same fold run_with_plan() will do). The plan is
built by hand here, because planner.py is not written yet at this point
in class. demo_plan_only.py works the same way.

Run:  python demo_react_vs_plan.py
Costs at least 3 API calls (1 plan call + at least 1 step each way).

Both runs get a higher step limit than the lab's MAX_STEPS, so the demo
does not stop at loop.py's 10-step limit before answering. This does not
change loop.py or MAX_STEPS. It only affects this script.

Both runs also use run_with_trace() below instead of agent.loop.run().
It is the same loop, with the same config, stopping rule and tools. It
is copied here only so a multi-line search_files() result prints on
separate lines. agent.loop.run() is unchanged, and it is still what
planner.py and the rest of the lab call.
"""

from google.genai import types

from agent import llm, tools
from agent.llm import generate, report
from agent.loop import find_function_call
from tasks import TASKS

LINE = "-" * 66
TASK = TASKS[0]
DEMO_MAX_STEPS = 20  # for this demo only. See the note above.


def run_with_trace(task: str, max_steps: int) -> str:
    """
    agent.loop.run(), copied here so this demo can print a multi-line tool
    result across several lines. Everything except that one print is the
    same as run(): config, stopping rule and tools. So the calls it makes,
    and their cost, match run().
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
print("Strategy 1: ReAct. Decide one step at a time, no plan.\n")
print(f'  task: "{TASK}"')

before = dict(llm.stats)
answer_reactive = run_with_trace(TASK, DEMO_MAX_STEPS)
after_reactive = dict(llm.stats)
calls_reactive = after_reactive["calls"] - before["calls"]

print(f"\n  answer: {answer_reactive}")
print(f"  cost:   {calls_reactive} calls")

print("\n" + LINE)
print("Strategy 2: plan-then-execute. Write the plan first, then run it.\n")

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
{calls_planned} calls planned. compare() in planner.py measures this gap
for you, on every task in tasks.py.

Neither strategy is always right. ReAct adapts as soon as a tool result
changes what is needed, and costs nothing extra up front. Plan-then-
execute picks an order before any tool call, and gives you a plan to
read and check first. But the plan can go out of date as soon as step
1's result changes what step 3 should be.
""")

report()
