"""
Week 6 demo · Dense vs. hybrid, side by side

Ranks four real files from data/ against one query, three ways: by
embedding similarity (dense), by keyword overlap, and by reciprocal rank
fusion (RRF) of those two rankings. It does not import agent.retrieval.
It does all three by hand on four files, like demo_retrieval.py. The
extension does the same over the whole indexed corpus, in
hybrid_retrieve() and compare_retrieval().

Run:  python demo_hybrid.py
      python demo_hybrid.py "your own query"
Costs 5 embed() calls (4 files + 1 query), every run. No generate() calls.
"""

import sys
from pathlib import Path

from agent.llm import embed, report

LINE = "-" * 66
DATA_DIR = Path(__file__).parent / "data"
FILES = ["ticket_001.txt", "ticket_009.txt", "refund_policy.txt", "pricing.txt"]
RRF_K = 60

query = sys.argv[1] if len(sys.argv) > 1 else "invoice INV-3381"
docs = {name: (DATA_DIR / name).read_text(encoding="utf-8") for name in FILES}


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b)


def keyword_score(query, text):
    """Same crude scorer as _keyword_score() in agent/retrieval.py."""
    words = {w for w in query.lower().split() if len(w) > 2}
    if not words:
        return 0.0
    text_lower = text.lower()
    return sum(1 for w in words if w in text_lower) / len(words)


def ranks(scores):
    """{name: score} -> {name: rank}, 1 = best."""
    order = sorted(scores, key=scores.get, reverse=True)
    return {name: i + 1 for i, name in enumerate(order)}


def show(title, scores, fmt):
    print(f"\n-- {title} --")
    for name in sorted(scores, key=scores.get, reverse=True):
        print(f"  {fmt.format(scores[name])}  {name}")


print(LINE)
print(f'query: "{query}"')
print(f"files: {', '.join(FILES)}")
print(LINE)

query_vec = embed(query)
dense = {name: cosine(query_vec, embed(text)) for name, text in docs.items()}
keyword = {name: keyword_score(query, text) for name, text in docs.items()}

dense_rank = ranks(dense)
keyword_rank = ranks(keyword)
fused = {
    name: 1 / (RRF_K + dense_rank[name]) + 1 / (RRF_K + keyword_rank[name])
    for name in docs
}

show("dense (embedding similarity)", dense, "{:.3f}")
show("keyword (fraction of query words found)", keyword, "{:.2f}")
show(f"hybrid (RRF: 1/({RRF_K}+dense rank) + 1/({RRF_K}+keyword rank))", fused, "{:.5f}")

top = {
    "dense": max(dense, key=dense.get),
    "keyword": max(keyword, key=keyword.get),
    "hybrid": max(fused, key=fused.get),
}
print(f"\ntop match:  dense {top['dense']}   keyword {top['keyword']}   hybrid {top['hybrid']}")
print("""
Where do the dense and keyword lists disagree, and which one did hybrid
side with? Only ticket_001.txt contains the exact ID. Which ranking would
you have trusted for this query? Then try a paraphrase that shares no
words with any file, and compare again.
""")

report()
