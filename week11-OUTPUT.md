# Week 11: OUTPUT

Name:
Date:

---

## 1. The demos

Paste the output of `python demo_handoff.py`.

```
paste here
```

**Q1.** Two of the five replies did not parse. For each one, say what the
next agent would have done with it if nothing had checked.

Paste the output of `python demo_roles.py`.

```
paste here
```

**Q2.** The planted handoff had a real quote. Which check caught it, the
string test or the model? Why could the other one not catch it?

---

## 2. Your team

Run one question with `--team` and paste the output, including the
researcher's handoff and the checker's verdict.

```
paste here
```

**Q3.** Did the checker find a problem? If it did, did the retry fix it? If
it did not, write a question that you think would make the checker reject
the first answer, run it, and paste what happened.

**Q4.** The checker can only use `read_file`. What could go wrong if it
also had `search_files`? Think about what it could do instead of checking
the file it was given.

**Q5.** In `checker()`, the code check runs before the model. Name one
other check in `team.py` that is done in code, and say why it does not
need a model.

---

## 3. Extension: test the checker

Required for everyone.

Paste the output of `python -m agent.team --test-checker`.

```
paste here
```

**Q6.** How many planted errors did it catch, and how many false alarms did
it raise? For any case it got wrong, say why you think it got it wrong.
Which case cost no API calls, and why?

**Q7.** Do you agree with every expected verdict in `checker_cases.py`? If
not, which one, and why?

---

## 4. Graduate extension: each agent separately

Required for COMP840.

Paste the output of `python -m agent.team --report`.

```
paste here
```

**Q8.** Which agent cost more, and why? How many handoffs parsed, and how
many quotes were really in the file?

**Q9.** Your project has at least two agents. Name one number from this
report you will measure for each of them, and how.

---

## 5. What broke

What went wrong while you were doing this, and what did you do about it?
