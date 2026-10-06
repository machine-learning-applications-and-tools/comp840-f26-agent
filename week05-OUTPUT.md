# Week 5: OUTPUT

Name:
Date:

---

## 1. The demo

Paste the output of `python demo_memory.py`.

```
paste here
```

**Q1.** The second call to `run()` in the demo never reads the JSON file
itself. The file's contents are folded into a plain string first. What
would the model actually see if you printed `folded` right before calling
`run()`?

---

## 2. Your memory

Paste the output of these two calls, in order:

```bash
python -m agent.cli --task "My favourite language is OCaml." --session me
python -m agent.cli --task "What is my favourite language?" --session me
```

```
paste here
```

**Q2.** Run a third call in the same session, asking something unrelated.
Does `with_memory()` still fold in the OCaml turn? Should it? What would
change your answer?

**Q3.** Open `memory/me.json` and paste its contents after your first two
calls. Is it readable enough that you could hand-edit it correctly if you
had to?

---

## 3. What memory does not fix

**Q4.** Start a brand new session and ask it to use a tool from Week 3
(the calculator, or a file lookup), across two separate `--session` calls
the way you did above. Does memory carry a tool RESULT across runs, or
only the plain task/answer text? Why? Point at the exact line in
`memory.py` that explains it.

---

## 4. Extension

Required for COMP840. Optional for COMP740.

**Q5.** Run at least 5 turns in one session, then call `summarize()` on it
from a Python shell. Paste the session file before and after.

**Q6.** Ask a question afterward that depends on something from BEFORE the
summarized turns. Does it still answer correctly? What did the summary
keep, and what did it lose?

---

## 5. What broke

What went wrong while you were doing this, and what did you do about it?
