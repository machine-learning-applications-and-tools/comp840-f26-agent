# Week 13: OUTPUT

Name:
Date:

---

## 1. The demo

Paste the output of `python demo_evaluate.py`.

```
paste here
```

**Q1.** Runs A and B give the same answer and both pass the outcome
check. Which one would you trust on a new task you had not seen before,
and why? What would an evaluation that only checked outcomes have told
you about Run B?

---

## 2. Your evaluation

Paste the output of a run on all six cases:

```bash
python -m agent.evaluate
```

```
paste here
```

**Q2.** Find a case where the outcome and the trajectory checks
disagree: one passed and the other failed. Run that case again with
`--trace` and paste its tool calls. Was the failing check right to fail,
or was the check itself too strict or too loose?

**Q3.** What did one full evaluation cost, in calls, tokens and time?
At 500 calls a day, how many full evaluations could you run? What does
that mean for how often you can afford to evaluate while you develop?

---

## 3. One run is not enough

**Q4.** Run the same two cases twice:

```bash
python -m agent.evaluate --cases 1 3
python -m agent.evaluate --cases 1 3
```

```
paste both here
```

Did any check, or the cost, change between the two runs? If you
reported only one of them, what would you be claiming that you have not
actually shown?

---

## 4. Benchmark

Required for everyone.

**Q5.** Paste the output of `python -m agent.evaluate --cases 1 3 --benchmark`.
If you skipped a strategy because its lab is not finished, say which.

```
paste here
```

**Q6.** Which strategy would you choose for these tasks, and why? Use the
outcome, the trajectory and the cost in your answer. Two cases is a small
sample. What would you need to run before you were sure?

---

## 5. What broke

What went wrong while you were doing this, and what did you do about it?
