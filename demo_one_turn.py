"""
Week 3 demo · One turn, by hand

Before you write the loop, watch one turn of it happen a step at a time.
This is the same thing tooltest.py did in Week 1, but now every step is
labelled with the box it belongs to.

Run:  python demo_one_turn.py
Costs 2 API calls.
"""

from google.genai import types

from agent import tools
from agent.llm import generate, report

LINE = "-" * 66

TASK = "What is 17 times 23, plus 100?"

config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=tools.schemas())],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

# ---------------------------------------------------------------- OBSERVE
print(LINE)
print("OBSERVE   what the model can see\n")

contents = [types.Content(role="user", parts=[types.Part(text=TASK)])]
print(f'    the task:   "{TASK}"')
print(f"    the tools:  {', '.join(tools.TOOLS)}")
print(f"    history:    {len(contents)} message so far")

# ------------------------------------------------------------------ THINK
print("\n" + LINE)
print("THINK     the model decides\n")

response = generate(contents, config=config)

call = None
for part in response.candidates[0].content.parts:
    if getattr(part, "function_call", None):
        call = part.function_call
        break

if call is None:
    print("    It answered directly, without using a tool:")
    print(f"    {response.text.strip()[:200]}")
    print("\n    Interesting. Run it again, it may not do that twice.")
    report()
    raise SystemExit

print(f"    It did not answer. It asked for a tool:\n")
print(f"        {call.name}({dict(call.args)})")
print(f"\n    That request is still just text. Nothing has run yet.")
print(f"    input tokens so far: {response.usage_metadata.prompt_token_count}")

# -------------------------------------------------------------------- ACT
print("\n" + LINE)
print("ACT       your code runs it\n")

result = tools.run(call.name, dict(call.args))
print(f"    tools.run({call.name!r}, {dict(call.args)})")
print(f"    returned:  {result!r}")
print("\n    This is the only step the model had nothing to do with.")

# ----------------------------------------------------------------- OBSERVE
print("\n" + LINE)
print("OBSERVE   round again, with the result added\n")

contents.append(response.candidates[0].content)
contents.append(types.Content(
    role="user",
    parts=[types.Part.from_function_response(
        name=call.name, response={"result": result})],
))
print(f"    history:    {len(contents)} messages now")
print("    Note we appended TWO things: what the model asked for, and what")
print("    the tool gave back. The transcript has to make sense as a")
print("    conversation or the model loses track of what it already did.")

# ------------------------------------------------------------------ THINK
print("\n" + LINE)
print("THINK     and this time it answers\n")

final = generate(contents, config=config)
print(f"    {final.text.strip()}")
print(f"\n    input tokens this call: {final.usage_metadata.prompt_token_count}")
print(f"    (it was {response.usage_metadata.prompt_token_count} last time. "
      "Every step resends everything.)")

print("\n" + LINE)
print("""
That was ONE turn. Two calls to the model, one tool run in between.

An agent is that, in a while loop, until the model stops asking for tools
and gives an answer instead.

Writing that loop is this week's lab. It is about fifteen lines, and they
are all in agent/loop.py waiting for you.
""")

report()
