"""
Weeks 7-8 demo · What a sub-agent buys you

Two runs of the same task, side by side:

  1. One agent does everything. Watch the input tokens grow on every
     step: each tool result stays in the conversation and gets sent
     again on every call after it.
  2. The same task, split BY HAND into two subtasks. Each worker is a
     fresh run() with its own conversation. The final combine call sees
     only the two workers' answers, never their tool calls.

This does not import agent.delegate. It does by hand what orchestrate()
has to do, so you see the mechanism before you write it.

Run:  python demo_subagent.py
Costs roughly 10 to 15 API calls.
"""

from agent import loop
from agent import llm
from agent.llm import generate, report

LINE = "-" * 66

# Record the input tokens of every call the loop makes, so we can show
# how big each prompt was. This wraps generate() for this demo only.
prompt_sizes = []


def _recording_generate(*args, **kwargs):
    response = generate(*args, **kwargs)
    usage = getattr(response, "usage_metadata", None)
    prompt_sizes.append(getattr(usage, "prompt_token_count", 0) or 0)
    return response


loop.generate = _recording_generate

TASK = (
    "A customer says they were charged twice. Find a support ticket about "
    "a similar case, check the refund policy, and say whether their "
    "charge would be refunded automatically."
)

print(LINE)
print("1. One agent, one conversation\n")
prompt_sizes.clear()
answer = loop.run(TASK, verbose=True)
single = list(prompt_sizes)
print("\n  input tokens per step:", single)
print("  the last step resends everything the agent has read so far")

print("\n" + LINE)
print("2. Two workers, each with a fresh conversation\n")

SUBTASKS = [
    "Find a support ticket about a customer who was charged twice, and "
    "summarize what happened in two sentences.",
    "Read the refund policy and say, in two sentences, whether duplicate "
    "charges are refunded automatically.",
]

answers, worker_sizes = [], []
for i, sub in enumerate(SUBTASKS, 1):
    prompt_sizes.clear()
    worker_answer = loop.run(sub, verbose=False)
    answers.append(worker_answer)
    worker_sizes.append(list(prompt_sizes))
    print(f"  worker {i} input tokens per step: {prompt_sizes}")
    print(f"  worker {i} hands back: {worker_answer[:160]}\n")

block = "\n\n".join(
    f"Worker {i} was asked: {s}\nWorker {i} answered: {a}"
    for i, (s, a) in enumerate(zip(SUBTASKS, answers), 1)
)
before = llm.stats["input_tokens"]
combined = generate(
    f"Task: {TASK}\n\nSeveral workers each handled one part of this task:"
    f"\n\n{block}\n\nCombine their answers into one answer to the task."
)
combine_tokens = llm.stats["input_tokens"] - before

print(f"  combine step input tokens: {combine_tokens}")
print(f"\n  combined answer: {combined.text.strip()[:300]}")

print("\n" + LINE)
print(f"""
Largest single prompt, one agent:     {max(single) if single else 0}
Largest single prompt, any worker:    {max(max(w) for w in worker_sizes if w) if any(worker_sizes) else 0}
Combine step:                         {combine_tokens}

No prompt in part 2 had to carry the whole task's history. Each worker
saw only its own subtask, and the combine step saw only two short
answers. That is context isolation. Count the total calls below before
deciding it was cheaper: it usually is not.
""")

report()
