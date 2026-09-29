"""
Week 5 demo · Recency isn't relevance

with_memory() folds in every saved turn. The extension's summarize() keeps
the most RECENT few and compresses the rest. Neither one asks whether an
older turn is actually the one a new question is about.

This builds five saved turns by hand, on five different topics -- same
{"task", "answer"} shape memory.py uses, but never imported from it, same
reason demo_memory.py builds its own JSON by hand. It shows which turns
summarize(keep_recent=3) would keep verbatim, then embeds all five tasks
plus a new question and ranks them by similarity instead of by recency.

Run:  python demo_semantic_recall.py
Costs 6 embed() calls. No generate() calls -- the saved answers below are
written by hand, since this demo is about which past TASK is relevant,
not about producing new answers.
"""

from agent.llm import embed, report

LINE = "-" * 66

turns = [
    {
        "task": "A customer was charged twice. Does that get refunded automatically?",
        "answer": "Only if the ticket matches the duplicate-charge pattern in the refund policy.",
    },
    {
        "task": "What is the difference in cost between the Growth and Scale plans?",
        "answer": "Scale costs 200 dollars more per month than Growth.",
    },
    {
        "task": "Several tickets complain about hitting the API rate limit.",
        "answer": "The Growth plan caps requests at 60 per minute.",
    },
    {
        "task": "A user cannot log in after resetting their password.",
        "answer": "Reset links expire after 30 minutes. Send a new one.",
    },
    {
        "task": "Can a customer export their ticket history to a CSV file?",
        "answer": "Yes, from the Reports page, one month at a time.",
    },
]

KEEP_RECENT = 3

new_task = "If a customer disputes a duplicate charge, what happens to it?"

print(LINE)
print("Five saved turns, oldest first\n")
for t in turns:
    print(f'  saved: "{t["task"]}"')
print(f'\n  new question: "{new_task}"')

print("\n" + LINE)
print(f"Recency: what summarize(keep_recent={KEEP_RECENT}) would do\n")
older, recent = turns[:-KEEP_RECENT], turns[-KEEP_RECENT:]
for t in recent:
    print(f'  kept verbatim:        "{t["task"]}"')
for t in older:
    print(f'  compressed away:      "{t["task"]}"')
print("\n  It picks by position. It never looks at the new question.")

print("\n" + LINE)
print("Semantic: embed every saved task and the new one, rank by similarity\n")


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b)


new_vec = embed(new_task)
scored = [(cosine(new_vec, embed(t["task"])), t) for t in turns]
scored.sort(key=lambda pair: pair[0], reverse=True)

for score, t in scored:
    print(f'  {score:.3f}  "{t["task"]}"')

best = scored[0][1]
print(f'\n  closest match: "{best["task"]}"')
if any(best is t for t in recent):
    print("  ...one summarize() would have kept anyway, this time.")
else:
    print("  ...one summarize() would have compressed away. Recency missed it.")

print("\n" + LINE)
print("""
This is not a replacement for summarize(). Budgeting (fewer tokens) and
relevance (the RIGHT tokens) are different problems, and you can have
either one without the other. Week 6 builds a real retrieval step out of
exactly this idea, against far more than five saved turns.
""")

report()
