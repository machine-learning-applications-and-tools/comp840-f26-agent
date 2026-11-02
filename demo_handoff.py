"""
Week 11 demo · What a handoff has to survive

Two checks that happen in code, before any agent trusts what another
agent sent it:

  1. Does the reply parse? Five replies a model might really send, run
     through parse_reply(). Only some of them give you a usable dict.
  2. Is the quote real? Three quotes run through quote_in_file(), a
     plain string test against the file in data/.

Uses only the given helpers in agent/team.py, so it works before you
write anything.

Run:  python demo_handoff.py
Costs 0 API calls.
"""

from agent.team import HANDOFF_FIELDS, parse_reply, quote_in_file

LINE = "-" * 66

REPLIES = [
    ("clean JSON",
     '{"answer": "$149 a month", "source": "pricing.txt", '
     '"quote": "Growth — $149/month"}'),
    ("wrapped in a code fence",
     '```json\n{"answer": "$149 a month", "source": "pricing.txt", '
     '"quote": "Growth — $149/month"}\n```'),
    ("a sentence before the JSON",
     'Here is my answer: {"answer": "$149 a month", '
     '"source": "pricing.txt", "quote": "Growth — $149/month"}'),
    ("a field missing",
     '{"answer": "$149 a month", "source": "pricing.txt"}'),
    ("no JSON at all",
     "The Growth plan costs $149 a month, according to pricing.txt."),
]

print(LINE)
print("1. Does the reply parse?\n")
for name, reply in REPLIES:
    result = parse_reply(reply, HANDOFF_FIELDS)
    status = "parsed" if result else "None"
    print(f"  {name:<28} -> {status}")

print("""
  The first three parse, because parse_reply() looks for the first
  {...} anywhere in the reply. The last two do not. A missing field is
  as bad as no JSON: the next agent would crash, or guess.
""")

QUOTES = [
    ("real, copied exactly", "Growth — $149/month", "pricing.txt"),
    ("real, but split across two lines in the file",
     "Duplicate or erroneous charges (billing errors, not cancellations) "
     "are refunded in full once confirmed, no discretion required.",
     "refund_policy.txt"),
    ("made up", "Email/password sessions last 7 days.",
     "security_overview.txt"),
]

print(LINE)
print("2. Is the quote really in the file?\n")
for name, quote, source in QUOTES:
    print(f"  {name:<46} -> {quote_in_file(quote, source)}")

print("""
  A made-up quote is caught by a string test, with no model call.
  Whether a REAL quote actually supports the answer is a different
  question. That one needs the checker.
""")
