"""
Week 13 demo · Same answer, different runs

Three runs of the agent, each checked by outcome (is the final answer
right?) and by trajectory (did it read the right files?).

The model's choices are scripted, so this costs nothing and gives the
same output every time. The tool calls are real and run against data/.

The checks here are simpler versions of the ones in agent/evaluate.py.

Run:  python demo_evaluate.py
Costs 0 API calls.
"""

from agent import tools
from eval_cases import CASES

LINE = "-" * 66

RUNS = [
    {
        "label": "Run A, case 0: looked it up",
        "case": 0,
        "calls": [
            ("search_files", {"query": "tax"}),
            ("read_file", {"name": "ticket_009.txt"}),
            ("read_file", {"name": "product_notes_billing.txt"}),
            ("calculator", {"expression": "499 * 0.0825"}),
        ],
        "answer": "ticket_009.txt disputes 8.25% tax on INV-3410. 8.25% of "
                  "$499 is $41.17. The billing notes say nothing about tax.",
    },
    {
        "label": "Run B, case 0: never looked",
        "case": 0,
        "calls": [],
        "answer": "8.25% of $499 is $41.17.",
    },
    {
        "label": "Run C, case 3: read the wrong file",
        "case": 3,
        "calls": [
            ("search_files", {"query": "alert"}),
            ("read_file", {"name": "ticket_008.txt"}),
            ("calculator", {"expression": "4 * 2"}),
        ],
        "answer": "The worst delay was 4 hours, so plan for 8 hours.",
    },
]


def outcome_ok(answer, case):
    """Every expected number appears somewhere in the answer."""
    words = answer.replace(",", "").replace("$", "").split()
    found = []
    for w in words:
        try:
            found.append(float(w.strip(".()%")))
        except ValueError:
            pass
    return all(any(abs(n - v) <= tol for n in found) for v, tol in case["numbers"])


def trajectory_ok(steps, case):
    """It read a required file, and used the required tools."""
    read = {args.get("name") for tool, args in steps if tool == "read_file"}
    used = {tool for tool, args in steps}
    return (all(group & read for group in case["must_read"])
            and all(group & used for group in case["must_use"]))


for run in RUNS:
    case = CASES[run["case"]]
    print(LINE)
    print(run["label"])
    print(LINE)
    for tool, args in run["calls"]:
        result = tools.run(tool, args)
        first = result.splitlines()[0] if result else ""
        print(f"  {tool}({args})")
        print(f"      -> {first[:58]}{' ...' if len(result) > len(first) else ''}")
    if not run["calls"]:
        print("  (no tool calls at all)")
    print(f"\n  answer: {run['answer']}")
    print(f"\n  outcome     {'PASS' if outcome_ok(run['answer'], case) else 'FAIL'}"
          f"   expected {[v for v, _ in case['numbers']]}")
    print(f"  trajectory  {'PASS' if trajectory_ok(run['calls'], case) else 'FAIL'}"
          f"   must read {[sorted(g) for g in case['must_read']]}\n")

print(LINE)
print("""
Runs A and B give the same answer and both pass the outcome check. Only
the trajectory check tells them apart. B got $41.17 without reading any
file, because the task gives 8.25% and $499. It never read the ticket,
so it never learned the customer says they are tax-exempt.

Run C fails both checks. It read a customer's ticket (2-4 hours) instead
of the postmortem (2-6 hours). The outcome check shows that it failed.
The trajectory check shows where.
""")
