"""
Week 11 demo · Two agents, two jobs

  1. What each role is given: its instructions and its tools. 0 calls.
  2. The researcher answers a question and hands over JSON.
  3. The checker gets two handoffs: the researcher's real one, and one
     with a wrong number planted in it. The quote in the planted one is
     real, so only the model can catch it.

This does not use researcher(), checker() or team(), which you write in
the lab. It does the same steps by hand with the given run_role().

Run:  python demo_roles.py
Costs roughly 6 to 10 API calls.
"""

from agent.llm import report
from agent.team import (
    CHECKER_INSTRUCTIONS, CHECKER_TOOLS, HANDOFF_FIELDS,
    RESEARCHER_INSTRUCTIONS, RESEARCHER_TOOLS, VERDICT_FIELDS,
    parse_reply, quote_in_file, run_role,
)

LINE = "-" * 66
QUESTION = "How much does the Scale plan cost per month?"

print(LINE)
print("1. Two roles\n")
print(f"  researcher tools: {RESEARCHER_TOOLS}")
print(f"  checker tools:    {CHECKER_TOOLS}")
print(f"\n  researcher instructions:\n    {RESEARCHER_INSTRUCTIONS}")
print(f"\n  checker instructions:\n    {CHECKER_INSTRUCTIONS}")

print("\n" + LINE)
print(f"2. The researcher, on: {QUESTION}\n")
reply = run_role(QUESTION, RESEARCHER_INSTRUCTIONS, RESEARCHER_TOOLS,
                 verbose=True)
handoff = parse_reply(reply, HANDOFF_FIELDS)
print(f"\n  raw reply: {reply.strip()}")
print(f"  parsed handoff: {handoff}")


def check(label, h):
    print(f"\n  {label}: {h}")
    if not quote_in_file(h["quote"], h["source"]):
        print("  code check: the quote is not in the file. Problem, 0 calls.")
        return {"verdict": "problem", "reason": "the quote is not in the file"}
    print("  code check: the quote is in the file. Asking the checker.")
    task = (f"Question: {QUESTION}\nAnswer: {h['answer']}\n"
            f"Source: {h['source']}\nQuote: {h['quote']}")
    verdict = parse_reply(
        run_role(task, CHECKER_INSTRUCTIONS, CHECKER_TOOLS, verbose=True),
        VERDICT_FIELDS,
    )
    print(f"  checker verdict: {verdict}")
    return verdict


print("\n" + LINE)
print("3. The checker, on two handoffs")
if handoff:
    check("the researcher's handoff", handoff)
else:
    print("\n  The researcher's reply did not parse, so there is nothing to check.")

planted = check("a planted wrong answer", {
    "answer": "$299 a month.",
    "source": "pricing.txt",
    "quote": "Scale — $499/month",
})

print("\n" + LINE)
print("\nThe checker never searched. It could only read the file it was pointed"
      "\nat. The planted handoff had a real quote, so the string test passed it.")
if planted is None or planted["verdict"] not in ("ok", "problem"):
    print("The model's verdict did not parse. In checker() that counts as a"
          "\nproblem, so the wrong answer would still not pass.\n")
elif planted["verdict"] == "problem":
    print("Only the model could see that $299 is not $499, and it did.\n")
else:
    print("This time the model passed it, so $299 got through. One run does"
          "\nnot show that a checker works. The extension tests it on six cases.\n")
report()
