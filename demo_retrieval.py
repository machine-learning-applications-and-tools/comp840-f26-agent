"""
Week 6 demo · Which document actually answers this?

Before you write index() and retrieve(), see embedding similarity rank
three candidate documents against one question. It does not import
agent.retrieval. It embeds three short texts and the query directly, the
same way demo_plan_only.py does not import agent.planner.

Run:  python demo_retrieval.py
Costs 4 embed() calls (3 documents + 1 query). No generate() calls.
"""

from agent.llm import embed, report

LINE = "-" * 66

candidates = {
    "refund_policy.txt": (
        "Duplicate or erroneous charges (billing errors, not cancellations) "
        "are refunded in full once confirmed, no discretion required."
    ),
    "pricing.txt": (
        "Growth costs $149/month with a 60 requests/minute API rate limit. "
        "Scale costs $499/month with a 300 requests/minute rate limit."
    ),
    "security_overview.txt": (
        "API keys are scoped per account and rotated on a 90-day "
        "grace-period cycle. Losing one means generating a new one."
    ),
}

query = "A customer was billed twice for the same period. What happens?"

print(LINE)
print("Three candidate documents, one query\n")
for name, text in candidates.items():
    print(f'  {name}\n    "{text}"\n')
print(f'  query: "{query}"')


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b)


print("\n" + LINE)
print("Embedding all four, ranking the three documents by similarity\n")

query_vec = embed(query)
scored = sorted(
    ((cosine(query_vec, embed(text)), name) for name, text in candidates.items()),
    reverse=True,
)
for score, name in scored:
    print(f"  {score:.3f}  {name}")

print(f"\n  top match: {scored[0][1]}")
print("""
refund_policy.txt answers the question, but it shares no key words with
it. The query says "billed twice". The policy says "duplicate or
erroneous charges". Embedding similarity compares meaning, not words, so
it can still rank the policy first. search_files() from Week 3 matches
exact text, so it would not find this match at all.
""")

report()
