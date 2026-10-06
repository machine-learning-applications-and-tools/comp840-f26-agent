# Week 6: Retrieval and grounding

COMP840 / COMP740 · ML Applications and Tools

New here? Start with the top-level `README.md` for one-time setup and
`UPDATING.md` for how to pull weekly updates. This file is this week's
instructions only.

## Pulling this week's files

Commit your own Week 5 work first. Then:

```bash
git fetch upstream
git checkout upstream/main -- README.md week06-README.md week06-OUTPUT.md .gitignore agent/cli.py agent/config.py agent/retrieval.py demo_retrieval.py demo_hybrid.py
git add -A
git commit -m "Pull Week 6 update"
```

What each one is for:

- `week06-README.md`, `week06-OUTPUT.md`, `agent/retrieval.py`,
  `demo_retrieval.py` and `demo_hybrid.py` are new this week.
- `README.md` gains one line pointing to this file.
- `.gitignore` now ignores `index/`, where the cached embeddings go. Pull
  it before your first `--retrieve` run, so you never commit the cache by
  accident. If you had added your own lines to `.gitignore`, add them back
  after the pull.
- `agent/cli.py` adds `--retrieve`.

Do not add `agent/loop.py`, `agent/tools.py`, `agent/planner.py` or
`agent/memory.py` to that list. Those are your own completed work from
Weeks 3 to 5, and pulling them would overwrite it. `tasks.py` and
`agent/llm.py` only have small comment changes, so you do not need to
pull them.

## What is here

```
agent/
    __init__.py     makes this a package
    config.py       the model names. Only place they appear.
    llm.py          generate() and embed(), with rate limiting and retries
    tools.py        the tools your agent can use
    loop.py         your Week 3 loop. Do not change it.
    planner.py      your Week 4 planner. Do not change it.
    memory.py       your Week 5 memory. Do not change it.
    retrieval.py    THE RETRIEVAL. This is the lab.
    cli.py          command line entry point, now with --retrieve
demo_one_turn.py    Week 3's demo, still here for reference
demo_plan_only.py, demo_react_vs_plan.py
                    Week 4's demos, still here for reference
demo_memory.py, demo_semantic_recall.py
                    Week 5's demos, still here for reference
demo_retrieval.py   watch embedding similarity pick the right document,
                    by hand, before you write retrieve()
demo_hybrid.py      dense, keyword and fused rankings side by side, on
                    four files, before you write hybrid_retrieve()
tasks.py            six tasks that need three or more tools in sequence
data/               the same 20 files Week 3's tools already point at
index/              cached embeddings land here once retrieval.py works
                    (gitignored, created at runtime)
```

Everything works except `retrieval.py`, as long as your loop, planner and
memory from Weeks 3 to 5 do.

## Run this first

```bash
python demo_retrieval.py
```

Four embed calls, no `generate()` calls. It ranks three short candidate
texts against one query by hand, so you see what similarity ranking looks
like before you write `index()` and `retrieve()`.

## The idea

Week 3 gave the agent `search_files()` and `read_file()`, tools the model
calls itself, mid-loop, one exact substring at a time. That is simple, and
it misses anything that does not share the query's exact words.

This week, before the loop starts, you rank every document in `data/` by
how similar its meaning is to the task, using embeddings instead of
substring matching, and fold the most relevant ones into the task text.
Same trick as Weeks 4 and 5: `loop.py` does not change. It just gets
handed a task string that already contains the right sources, labelled,
with an instruction to cite them.

## The lab

Open `agent/retrieval.py`. `load_corpus()` is given. Three functions are
not:

- `index()`: embed every file in `data/` once, and cache the result to
  `index/embeddings.json`. Without the cache, every query would re-embed
  the whole corpus.
- `retrieve(query, top_k=3)`: rank the cached embeddings by cosine
  similarity to `query`, and return the best matches.
- `with_retrieval(task, top_k=3)`: fold those matches into `task`,
  labelled by source, with an instruction to cite them.

Test it:

```bash
python -m agent.cli --task "What happens if a customer is charged twice?"
--retrieve
```

The first call costs 20 embed calls (indexing the corpus), plus 1 for the
query, plus whatever `loop.run()` needs. Every call after that costs 1
embed call plus the loop, until you delete `index/`. Indexing takes about a
minute and a half, because `embed()` paces itself to stay under the rate
limit. That is normal, not a hang.

## Reading

Required for everyone, COMP840 and COMP740.

Read the Generative Agents paper (Park et al., 2023) up to the end of
Section 4, "Generative Agent Architecture":
https://arxiv.org/abs/2304.03442

It is about agents that remember. Its memory is a saved record of
everything an agent did, and it retrieves memories by how recent,
important and relevant they are. That is Week 5's memory and this
week's retrieval in one design.

Write 2 to 3 questions about it in `week06-OUTPUT.md`. The best questions
connect the paper to something you have built or run, such as `memory.py`,
`summarize()` or `retrieve()`, or ask why one of its design choices works
and when it would fail. Avoid questions the paper answers in a single
sentence, or that only ask for a definition.

Then write a short reflection, one paragraph: what stood out to you in
the paper, and how does it connect to the agent you have been building?

## Extension

Required for COMP840. Optional but encouraged for COMP740.

- **Hybrid search.** `retrieve()` only asks "what looks similar in
  meaning." An exact invoice ID or plan name is not a "similar idea"
  question, and embeddings are not built for exact matches. Fill in
  `hybrid_retrieve()` and `compare_retrieval()` at the bottom of
  `agent/retrieval.py`. Rank documents by both dense similarity and plain
  keyword overlap, and merge the two rankings with reciprocal rank fusion.

  Run `python demo_hybrid.py` first. It does the same three rankings by
  hand on four files, so you can see what you are building. Five embed
  calls per run. Pass your own query in quotes to try another one.

  Then answer Q5 and Q6 in `week06-OUTPUT.md`.

## Do not change the entry point

`python -m agent.cli --task "..."` has to keep working exactly as it does
now. `--retrieve` is new and optional. It does not replace the default
behavior. In Week 12 you will run each other's agents, and that only works
if they are all invoked the same way.

## Watch your quota

15 requests a minute, 500 a day, for `generate()`. `embed()` calls go to
`EMBED_MODEL`, which has its own separate budget: 100 requests a minute,
30,000 tokens a minute, and 1,000 requests a day on the free tier. You can
see your own usage against these on your [AI Studio rate-limit
page](https://aistudio.google.com/rate-limit).

Indexing the corpus costs 20 embed calls, but only once. `index()` caches
to disk so you do not pay that on every test run. Make sure the cache
actually works before you start iterating. If `index/embeddings.json`
looks stale, or you changed anything in `data/`, delete it and let it
rebuild rather than editing it by hand.

If something goes wrong, stop it with Ctrl+C rather than letting it run.

## Submitting

Fill in `week06-OUTPUT.md`, including your reading questions and
reflection, and commit everything, including your code. Do not commit
anything under `index/`. It is gitignored on purpose.

**Due 11:59pm Monday.**
