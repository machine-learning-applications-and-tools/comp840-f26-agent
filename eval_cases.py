"""
The evaluation cases for Week 13. Given.

One case per task in tasks.py, in the same order. The comment next to
each expected value says which file in data/ it came from.

Fields:
    task            the task text, straight from tasks.py
    numbers         numbers the final answer must contain, as
                    (value, tolerance) pairs. Empty when the answer is a
                    decision in words, which code cannot check.
    must_read       files the agent must have opened with read_file().
                    Each entry is a set: reading ANY file in the set
                    counts. {"a.txt", "b.txt"} means "a or b".
    must_use        tools the agent must have called at least once.
                    Same rule: each entry is a set of acceptable tools.
    max_tool_calls  more tool calls than this is wasteful for this task.
    reference       a correct answer in plain words, for a person to
                    compare against.
"""

from tasks import TASKS

ARITHMETIC = {"calculator", "run_python"}

CASES = [
    {
        "task": TASKS[0],
        # 8.25% of $499 = 41.1675, so $41.17. The task itself gives both
        # numbers, so a run can get this right without opening any file.
        "numbers": [(41.17, 0.01)],
        "must_read": [{"ticket_009.txt"}, {"product_notes_billing.txt"}],
        "must_use": [ARITHMETIC],
        "max_tool_calls": 8,
        "reference": (
            "ticket_009.txt disputes 8.25% sales tax on invoice INV-3410: "
            "the customer is a nonprofit and says the account should be "
            "tax-exempt. 8.25% of $499 is $41.17. The billing notes say "
            "nothing about tax."
        ),
    },
    {
        "task": TASKS[1],
        # pricing.txt: Growth $149/month, Scale $499/month.
        # 499 - 149 = 350 a month. 350 * 12 = 4,200 a year.
        "numbers": [(350, 0), (4200, 0)],
        "must_read": [{"pricing.txt"}],
        "must_use": [ARITHMETIC],
        "max_tool_calls": 6,
        "reference": (
            "Scale is $499 a month and Growth is $149, a difference of "
            "$350 a month, so switching saves $4,200 over a year of "
            "monthly billing."
        ),
    },
    {
        "task": TASKS[2],
        # ticket_008.txt: alert emails 2-4 hours late for three days,
        # in-app notifications on time. product_notes_notifications.txt:
        # "If a customer says in-app alerts are timely but email is
        # delayed, this is the queue, not a bug in our alerting logic."
        "numbers": [],
        "must_read": [{"ticket_008.txt"}, {"product_notes_notifications.txt"}],
        "must_use": [{"search_files", "list_files"}],
        "max_tool_calls": 8,
        "reference": (
            "ticket_008.txt: alert emails arriving 2-4 hours late for the "
            "past three days, while in-app notifications are on time. The "
            "notification notes say that exact pattern is the mail "
            "provider's queue, not a bug in the alerting logic. So it is "
            "the same known cause as September, not a new bug. It is "
            "worth flagging that it has recurred, since the postmortem's "
            "fix (a dedicated sending tier) has no committed date."
        ),
    },
    {
        "task": TASKS[3],
        # outage_postmortem.txt: "Alert emails queued behind it were
        # delayed by 2-6 hours." Worst delay 6 hours, twice that = 12.
        "numbers": [(12, 0)],
        "must_read": [{"outage_postmortem.txt"}],
        "must_use": [ARITHMETIC],
        "max_tool_calls": 6,
        "reference": (
            "The mail provider's shared sending queue backed up after a "
            "spike from another customer. The postmortem says alert "
            "emails were delayed by 2 to 6 hours. The worst delay was 6 "
            "hours, so the team should plan for 12 hours."
        ),
    },
    {
        "task": TASKS[4],
        # refund_policy.txt: "Duplicate or erroneous charges ... are
        # refunded in full once confirmed, no discretion required."
        # ticket_001.txt is the similar case (INV-3381 and INV-3382).
        "numbers": [],
        "must_read": [{"ticket_001.txt"}, {"refund_policy.txt"}],
        "must_use": [{"search_files", "list_files"}],
        "max_tool_calls": 8,
        "reference": (
            "Yes, it qualifies. refund_policy.txt says duplicate or "
            "erroneous charges are refunded in full once confirmed, with "
            "no discretion required. ticket_001.txt is a similar case "
            "(INV-3381 and INV-3382). Confirm the duplicate against the "
            "two invoice IDs before issuing the refund. No exception is "
            "needed beyond that check."
        ),
    },
    {
        "task": TASKS[5],
        # ticket_007.txt: region column missing from CSV export since
        # last week's update. changelog.txt, v2.14.0: "CSV export now
        # includes the region column in all cases (web only)."
        "numbers": [],
        "must_read": [{"ticket_007.txt"}, {"changelog.txt"}],
        "must_use": [{"search_files", "list_files"}],
        "max_tool_calls": 8,
        "reference": (
            "ticket_007.txt reports the region column missing from CSV "
            "exports since last week's update. changelog.txt says v2.14.0 "
            "made CSV export include the region column in all cases, but "
            "web only. So it is fixed for web exports in v2.14.0. The "
            "ticket does not say web or mobile, so ask. On mobile it is "
            "not covered by that fix."
        ),
    },
]

