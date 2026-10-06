"""
Retrieval and grounding.

This file is the lab. Everything else already works, including loop.py,
planner.py and memory.py. You are not changing any of them.

Weeks 4 and 5 each folded something into the task string before handing
it to run(): a plan, then prior turns. This week folds in the parts of
data/ that look relevant to the question, using the same trick. The loop
still does not change. It just gets a longer task string.

How this differs from Week 3's search_files(): search_files() matches
exact substrings, and the model calls it during the loop, one query at a
time. Retrieval here ranks by meaning using embeddings, and runs once,
before the loop starts. That makes it closer to Week 4's plan than to
Week 3's tools.
"""

import json
from pathlib import Path

from agent.llm import embed

DATA_DIR = (Path(__file__).parent.parent / "data").resolve()
INDEX_PATH = (Path(__file__).parent.parent / "index" / "embeddings.json").resolve()


def load_corpus() -> list[dict]:
    """
    Every .txt file in data/, as {"source": filename, "text": contents}.

    Given, not part of the lab. It reads the whole folder at once, which
    is what index() below needs.
    """
    docs = []
    for path in sorted(DATA_DIR.glob("*.txt")):
        docs.append({"source": path.name, "text": path.read_text(encoding="utf-8")})
    return docs


def index() -> list[dict]:
    """
    Embed every document in load_corpus() once, and cache the result.

    Returns a list of {"source": ..., "text": ..., "embedding": [...]}.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  If INDEX_PATH already exists, load and return it instead of
        embedding anything:

            if INDEX_PATH.exists():
                return json.loads(INDEX_PATH.read_text())

        Without this cache, every call to retrieve() embeds all 20
        documents again before it can answer one query. That is 20 calls
        for a question that needed 1.

    2.  Otherwise, for each doc in load_corpus(), call embed(doc["text"])
        and store the result as doc["embedding"].

    3.  Write the whole list to INDEX_PATH as JSON, then return it. Make
        the folder first: INDEX_PATH.parent.mkdir(exist_ok=True)

    The first run costs 20 embed calls. Later runs cost 0, until someone
    deletes index/.
    """
    raise NotImplementedError("write the index")


def _cosine(a: list[float], b: list[float]) -> float:
    """Given. The similarity score retrieve() ranks by."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b)


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """
    The top_k documents most similar to `query`, best match first.

    Returns a list of {"source": ..., "text": ..., "score": ...}. Leave out
    the embedding. The caller does not need it.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  docs = index(). This reads the cache almost every time.

    2.  query_vec = embed(query). This is the one embed call retrieve()
        always makes.

    3.  Score every doc with _cosine(query_vec, doc["embedding"]).

    4.  Sort by score, highest first, and return the top_k as
        {"source": doc["source"], "text": doc["text"], "score": score}.
    """
    raise NotImplementedError("write retrieve")


def with_retrieval(task: str, top_k: int = 3) -> str:
    r"""
    Fold the top_k retrieved documents into task, the same way Week 4
    folded in a plan and Week 5 folded in prior turns.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  results = retrieve(task, top_k). If it comes back empty, return
        task unchanged.

    2.  Build one block per result, labelled with its source, so an
        answer can point back to where it came from:

            "\n\n".join(
                f"[source: {r['source']}]\n{r['text']}" for r in results
            )

    3.  Return task with that block in front, and an instruction to cite
        the sources. Having the text in the prompt does not make the
        model cite it.

            f"Use the following sources to answer. Cite the source "
            f"filename for every claim you make.\n\n{block}\n\n"
            f"Question: {task}"

    Do not save anything here. As with with_memory(), callers pass the
    original task to memory.save(), not this folded one.
    """
    raise NotImplementedError("write with_retrieval")


# =======================================================================
# GRADUATE EXTENSION. COMP840 required, COMP740 optional.
#
# retrieve() ranks by meaning, so it treats "duplicate charge" and
# "double charge" as the same idea. A query for an exact invoice ID or
# error code is different: it needs an exact match, and embeddings are
# not built for that. Hybrid search ranks both ways and merges the two.
# =======================================================================

def _keyword_score(query: str, text: str) -> float:
    """
    Given. A simple keyword scorer, not real BM25.

    The fraction of the query's words (lowercased, longer than 2
    letters) that appear anywhere in text. It is kept simple because this
    extension is about reciprocal rank fusion, not about search engines.
    """
    words = {w for w in query.lower().split() if len(w) > 2}
    if not words:
        return 0.0
    text_lower = text.lower()
    hits = sum(1 for w in words if w in text_lower)
    return hits / len(words)


def hybrid_retrieve(query: str, top_k: int = 3) -> list[dict]:
    """
    Rank documents by dense similarity and by keyword overlap, and merge
    the two rankings with reciprocal rank fusion (RRF).

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  docs = index(). Score every doc two ways: dense = _cosine against
        embed(query), and keyword = _keyword_score(query, doc["text"]).

    2.  Rank the docs by dense score, and separately by keyword score.
        Each doc now has two ranks (1 = best).

    3.  Fuse the ranks, not the scores:
        fused_score = 1/(60 + dense_rank) + 1/(60 + keyword_rank).
        60 is the usual RRF constant. It keeps the gaps between ranks
        small, so neither ranking decides on its own.

    4.  Sort by fused_score, highest first, and return the top_k in the
        same shape as retrieve(), with "score" set to the fused score.
    """
    raise NotImplementedError("write hybrid_retrieve")


def compare_retrieval(query: str, top_k: int = 3) -> None:
    """
    Run retrieve() and hybrid_retrieve() on the same query and print both
    rankings, so you can see where they agree and where they do not.

    Returns nothing. It is meant to be read as it prints, like Week 4's
    compare().

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  dense = retrieve(query, top_k)
        hybrid = hybrid_retrieve(query, top_k)

    2.  Print both lists in rank order, with source and score.

    3.  Print which sources appear in one list but not the other.

    Answer in week06-OUTPUT.md: try one query built around an exact word,
    such as an invoice ID or a plan name, and one paraphrase that shares
    no words with any file. Does hybrid change the top result on either?
    """
    raise NotImplementedError("write compare_retrieval")
