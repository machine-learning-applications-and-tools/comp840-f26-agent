# Week 3 — OUTPUT

Name:
Date:

---

## 1. The demo

Paste the output of `python demo_one_turn.py`.

```
paste here
```

The input token count went up between the first call and the second. By how
much, and why?

---

## 2. Your loop

Paste the output of a successful run:

```bash
python -m agent.cli --task "A Scale plan costs 499 dollars a month. What would 6 months cost, minus a 150 dollar loyalty discount?"
```

```
paste here
```

**Q1.** Your loop appends two things to `contents` each time round. What
breaks if you only append the tool result and not the model's request?
Try it, and describe what actually happens.

**Q2.** How many API calls did that one task take? How many would a task
needing three tools in sequence take?

---

## 3. Your classifier as a tool

Paste a run where the agent uses your classifier:

```
paste here
```

**Q3.** In Week 2 your classifier had to parse JSON out of a text reply. What
does it return now, and did you still need the parsing? Why or why not?

**Q4.** Write down the description you gave the tool. Then try making it
vaguer and run it again. Did the model still call it correctly?

---

## 4. Multiple tools in one run

Paste a run where the agent uses more than one tool in sequence:

```bash
python -m agent.cli --task "Are we able to refund a duplicate charge? Check the tickets and the policy."
```

```
paste here
```

**Q5.** How many tool calls did it make, and in what order? Does that match
what you would expect from the task, or did it search more (or less) than
seemed necessary?

Optional: try a task of your own that needs at least two tools, and paste
that run too.

```
paste here (optional)
```

---

## 5. Extension

Required for COMP840.

**Q6.** What does your loop do when `max_steps` runs out? How would the
caller know that happened, rather than the agent having finished?

**Q7.** Make the calculator fail, by asking the agent something like "what is
seventeen times twenty three" in words. What happened? Should a tool failure
crash the loop, or go back to the model? Argue for one.

---

## 6. What broke

What went wrong while you were doing this, and what did you do about it?
