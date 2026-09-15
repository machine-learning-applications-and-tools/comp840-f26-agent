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

TASK = "A Scale plan costs 499 dollars a month. What would 6 months cost, minus a 150 dollar loyalty discount?"

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

# response.candidates is a list because the API lets you ask for several
# alternative replies to the same prompt in one call. We never ask for
# more than one, so there is always exactly one candidate here. [0] is
# just unwrapping that list -- it is not picking a "best" reply out of
# several, there is only ever the one.
call = None
for part in response.candidates[0].content.parts:
    # content.parts is ALSO a list, for a different reason: a single
    # reply can contain more than one piece, for example some text AND a
    # function call together. So you cannot assume the part you want is
    # parts[0] -- you have to look through all of them and check each one.
    if getattr(part, "function_call", None):
        call = part.function_call
        break

if call is None:
    print("    It answered directly, without using a tool:")
    print(f"    {response.text.strip()[:200]}")
    print("\n    Interesting. Run it again, it may not do that twice.")
    report()
    raise SystemExit

# The model sends back two things here: call.name, a plain string naming
# which tool it wants (it has to match a name in TOOLS), and call.args, a
# dictionary of arguments whose keys match the parameters in that tool's
# own schema. Neither of these has run anything -- this is still just the
# model describing what it would like to happen next.
print(f"    It did not answer. It asked for a tool:\n")
print(f"        {call.name}({dict(call.args)})")
print(f"\n    That request is still just text. Nothing has run yet.")
print(f"    input tokens so far: {response.usage_metadata.prompt_token_count}")

# -------------------------------------------------------------------- ACT
print("\n" + LINE)
print("ACT       your code runs it\n")

# This print only DISPLAYS the call, one line before it happens. The text
# inside the quotes is a string, not code -- nothing runs when you print
# it. Printing it first, then running it, is why this line comes before
# the next one instead of after.
print(f"    tools.run({call.name!r}, {dict(call.args)})")

# This is the line where something actually happens. Every line before
# this one in the whole script has been text: read out of a reply,
# printed to the screen, copied from one variable to another. This is the
# first line that touches anything outside this process.
result = tools.run(call.name, dict(call.args))
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
