"""
Six tasks for the planner.

Each one needs at least three tool calls in sequence -- some combination
of list_files, search_files, read_file, and calculator -- against the
data/ files list_files/read_file/search_files already point at. None of
these are answerable from a single tool call, and none are answerable by
guessing; each one requires actually looking something up before the
arithmetic (or the final answer) makes sense.

Given, not an exercise. Run the planner against these once it works:

    python -c "from agent.planner import run_with_plan; \\
               from tasks import TASKS; print(run_with_plan(TASKS[0]))"
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

    "Find out why alert emails were delayed in September, read the "
    "postmortem, and calculate how many hours the worst delay was, "
    "doubled, for a follow-up report to the team.",

    "A customer says they were charged twice and wants to know if that "
    "gets refunded automatically or needs a ticket. Check the support "
    "tickets for a similar case, then check the refund policy, and tell "
    "me whether their charge would qualify.",

    "A customer says the CSV export used to include a 'region' column "
    "but a recent download is missing it. Find their ticket, check the "
    "changelog for anything relevant, and tell me whether this is "
    "already fixed or still an open bug.",
]
