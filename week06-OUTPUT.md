# Week 6: OUTPUT

Name:
Date:

---

## 1. The demo

Paste the output of `python demo_retrieval.py`.

```
paste here
```

**Q1.** The winning document did not share the query's exact words. What
in the demo's output tells you that, and why did embedding similarity
still rank it first?

---

## 2. Your retrieval

Run these two calls, in order, and paste both outputs:

```bash
python -m agent.cli --task "What happens if a customer is charged twice?"
--retrieve
python -m agent.cli --task "How much does the Growth plan cost?" --retrieve
```

```
paste here
```

**Q2.** Open `index/embeddings.json` after the first call. How many embed
calls did indexing cost, and how many did the second `--retrieve` call
cost? Point at the line in `retrieval.py` responsible for the difference.

**Q3.** Pick one of your two answers above and check it against the actual
source file it cited. Does the citation match a real claim in that file,
or did the model cite a source without actually using it?

---

## 3. What retrieval does not fix

**Q4.** Ask a question that no file in `data/` can answer. Paste the task and the answer. Did the agent say so
plainly, invent something plausible-sounding, or something in between?

---

## 4. Reading

Required for everyone, COMP840 and COMP740.

Read the Generative Agents paper (Park et al., 2023) up to the end of
Section 4: https://arxiv.org/abs/2304.03442

Write 2 to 3 questions about it. The best questions connect the paper to
something you have built or run, such as `memory.py`, `summarize()` or
`retrieve()`, or ask why one of its design choices works and when it would
fail. Avoid questions the paper answers in a single sentence, or that only
ask for a definition.

**R1.**

**R2.**

**R3.** (if you have a third)

**Reflection.** One paragraph: what stood out to you in the paper, and
how does it connect to the agent you have been building?

---

## 5. Extension

Required for COMP840.

**Q5.** Run `compare_retrieval()` from a Python shell on a query built
around an exact word (an invoice ID, a plan name) and a second query
built as a paraphrase sharing no words with any document. Paste both
outputs.

**Q6.** On which of the two queries, if either, did hybrid search return
a different top result than dense retrieval alone? Does that match what
you'd expect from combining a semantic signal with a keyword signal?

---

## 6. What broke

What went wrong while you were doing this, and what did you do about it?
