"""
Week 4 demo · Watch a plan get written

Before you write make_plan(), watch what one raw call for a plan actually
returns. This does not import agent.planner -- it makes the exact call
make_plan() has to make, by hand, so you see the real shape of a reply
before you write code that has to parse it.

Run:  python demo_plan_only.py
Costs 1 API call.
"""

from agent.llm import generate, report
from tasks import TASKS

LINE = "-" * 66

TASK = TASKS[0]

print(LINE)
print("Asking for a plan, no tools attached\n")
print(f'    the task:  "{TASK}"')

response = generate(
    "Before doing anything, write a short numbered plan for this task. "
    "One short step per line, no more than five steps, plain language, "
    "no code.\n\n"
    f"Task: {TASK}"
)

print("\n" + LINE)
print("What came back\n")
print(response.text)

print("\n" + LINE)
print("""
That reply is everything make_plan() has to work with. Run this a second time and compare the
formatting before you write your parser.
""")

report()
