# Weeks 7-8: OUTPUT

Name:
Date:

---

## Tuesday: sandboxing

## 1. The demo

Paste the output of `python demo_sandbox.py`.

```
paste here
```

**Q1.** Part 2 of the demo runs the leaking code as a separate process,
and it still leaks. What about how `subprocess.run()` is called in Part 2
causes that, and what one argument in Part 3 changes it?

---

## 2. Your sandbox

Run these two calls, in order, and paste both outputs:

```bash
python -m agent.cli --task "Use Python to compute the 15th Fibonacci number."
python -m agent.cli --task "Use Python to run: while True: pass"
```

```
paste here
```

**Q2.** Did the second call hang, time out cleanly, or crash the agent?
Point at the line in `run_python()` responsible.

**Q3.** Check both functions on the demo's environment snippet, and paste
the output:

```bash
python -m agent.sandbox
```

```
paste here
```

Why does one print the secret and the other print `None`?

**Q4.** Without running it: would `import socket` work inside
`run_python_contained()`? What does that tell you about calling it
"sandboxed"?

---

## Wednesday: sub-agents

## 3. The demo

Paste the output of `python demo_subagent.py`.

```
paste here
```

**Q5.** Compare the largest single prompt in Part 1 with the largest in
Part 2, and the total calls of each. Which one used fewer tokens per
prompt? Which one used fewer calls? Why are both true?

---

## 4. Your orchestrator

Run one task from `tasks.py` with `--orchestrate` and paste the output,
including the subtasks it chose.

```
paste here
```

**Q6.** Was the split a good one? Could each subtask really be done by
someone who had not seen the others? If not, which one depended on
another, and what happened to it?

**Q7.** What could a worker see while it ran, and what could it not see?
Point at the line in `run_worker()` that decides this.

---

## 5. Extension

Required for COMP840.

**Q8.** Paste the output of `compare()` on one task from `tasks.py`.

**Q9.** Which version cost more in total, and where did the orchestrated
version's tokens go? Compare the combine step's input tokens with the
single agent's. What does that say about context isolation, and does it
make the orchestrated version better for this task?

---

## 6. What broke

What went wrong while you were doing this, and what did you do about it?
