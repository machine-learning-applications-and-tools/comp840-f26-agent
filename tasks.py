"""
Six tasks for the agent, used since Week 4.

Each one needs at least three tool calls in a row, using some mix of
list_files, search_files, read_file and calculator on the files in data/.
None can be answered with a single tool call or by guessing. Each one
needs something looked up before the arithmetic or the final answer makes
sense.

Given, not an exercise. Week 4 ran the planner on them. In Week 13,
eval_cases.py gives the expected answer for each one, and
agent/evaluate.py checks a run against it:

    python -m agent.evaluate
"""

TASKS = [
    "One ticket disputes a tax charge. Find it, check the billing notes "
    "for anything relevant, and calculate what an 8.25% tax on a $499 "
    "Scale-plan invoice should actually come to.",

    "What is the difference in monthly cost between the Growth and Scale "
    "plans, and how much would a customer switching from Scale down to "
    "Growth save over a full year?",

    "A different customer also complains that alert emails are arriving "
    "late, well after the known September incident. Find their ticket, "
    "check the notification product notes, and tell me whether this "
    "looks like the same known issue or something new that needs "
    "escalating.",

    "Find out why alert emails were delayed in September and read the "
    "postmortem. What was the worst delay, in hours? The team wants to "
    "plan for twice that. How many hours should they plan for?",

    "A customer says they were charged twice and wants to know if that "
    "gets refunded automatically or needs a ticket. Check the support "
    "tickets for a similar case, then check the refund policy, and tell "
    "me whether their charge would qualify.",

    "A customer says the CSV export used to include a 'region' column "
    "but a recent download is missing it. Find their ticket, check the "
    "changelog for anything relevant, and tell me whether this is "
    "already fixed or still an open bug.",
]
