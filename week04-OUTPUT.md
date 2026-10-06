# Week 4: OUTPUT

Name:
Date:

---

## 1. Your planner

Paste the output of one successful `--plan` run from `tasks.py`:

```bash
python -m agent.cli --task "..." --plan
```

```
paste here
```

**Q1.** Paste the plan the model wrote, exactly as `make_plan()` returned
it. Did the loop underneath follow it step by step, or did it depart from
the plan at any point? If it departed, was that a problem?

**Q2.** How many API calls did this task take in total, counting the
planning call and every step of the loop? How does that compare to what the same task
would have cost reactively, without a plan?

---

## 2. Across the six tasks

Run your planner against at least three tasks from `tasks.py`.

**Q3.** Pick the task where the plan was least useful: ignored by the
loop, wrong about which tools were needed, or just restating the task
without breaking it into real steps. Paste the plan and say what was wrong
with it.

**Q4.** `make_plan()` has to parse the model's reply into a list of steps.
What format did the model actually use when you ran it (numbered, dashed,
something else)? Did your parsing handle it on the first try?

---

## 3. Comparing all six

Run `compare()` on **all six** tasks from `tasks.py`. Required for everyone.

**Q5.** Paste the output (both answers, both cost lines) for **three**
tasks that show three different outcomes:

- one where planning **won**: cheaper, a clearly better answer, or both
- one that was a **near-tie**: no real difference either way
- one where **reactive won**: planning cost more calls or tokens for no
  real benefit, or gave a worse answer

**Q6.** Across all six tasks, is there a pattern to which way a task
goes? For example task length, how much the tools need a specific order,
or something else. What would make you trust that pattern, given six tasks on one
model?

---

## 4. Extension

Required for COMP840.

**Q7.** Paste one run where `reflect()` retried (the critique found a real
problem) and one where it did not. Did the retry's answer actually improve,
or did it just cost two more calls for the same result?

---

## 5. What broke

What went wrong while you were doing this, and what did you do about it?
