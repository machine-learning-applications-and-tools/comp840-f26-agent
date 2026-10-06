"""
Week 5 demo · Memory, by hand

Before you write agent/memory.py, watch two separate "runs" pass
information between each other using nothing but a JSON file on disk.
It does not import agent.memory. It does by hand what load() and
save() have to do, so you see how it works before you write it.

Run:  python demo_memory.py
Costs 2 API calls.
"""

import json
from pathlib import Path

from agent.llm import report
from agent.loop import run

LINE = "-" * 66
DEMO_FILE = Path("demo_memory.json")

print(LINE)
print("Run 1: a fresh session, nothing saved yet\n")

task1 = "My favourite programming language is OCaml. Remember that."
print(f'  task: "{task1}"')
answer1 = run(task1, verbose=False)
print(f"  answer: {answer1}")

DEMO_FILE.write_text(json.dumps([{"task": task1, "answer": answer1}]))
print(f"\n  saved to {DEMO_FILE}")

print("\n" + LINE)
print("Run 2: a brand new call to run(), no shared memory except that file\n")

saved = json.loads(DEMO_FILE.read_text())
block = "\n".join(f"You: {t['task']}\nYou answered: {t['answer']}" for t in saved)
task2 = "What is my favourite programming language?"
folded = f"Earlier in this conversation:\n{block}\n\nNow: {task2}"

print(f'  task, folded with memory:\n\n"{folded}"\n')
answer2 = run(folded, verbose=False)
print(f"  answer: {answer2}")

print("\n" + LINE)
print("""
Nothing about run() changed between these two calls. Both times it built
a fresh contents list from one task string and ran the same loop. The
only thing that changed is the string it was handed, just like
Week 4's plan.
""")

DEMO_FILE.unlink(missing_ok=True)
report()
