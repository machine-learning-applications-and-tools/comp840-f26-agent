"""
Exercise · Two broken loops

Both functions below look like reasonable attempts at agent/loop.py. Each
is wrong in a different way. Neither raises an exception or prints an
obvious error, so running one will not tell you what is wrong on its own
— you have to trace the logic.

The task: for each function, find the bug and write down, in your own
words, what goes wrong and why. Do not fix them. That is a separate
exercise.
"""

from google.genai import types

from agent import tools
from agent.llm import generate
from agent.loop import MAX_STEPS, find_function_call


def loop_a(task: str) -> str:
    """Run the agent until it answers."""
    config = types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=tools.schemas())],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
    )
    contents = [types.Content(role="user", parts=[types.Part(text=task)])]

    response = generate(contents, config=config)
    call = find_function_call(response)

    while True:
        if call is None:
            return response.text

        contents.append(response.candidates[0].content)
        result = tools.run(call.name, dict(call.args))
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_function_response(
                name=call.name, response={"result": result},
            )],
        ))
        response = generate(contents, config=config)


def loop_b(task: str, max_steps: int = MAX_STEPS) -> str:
    """Run the agent until it answers, or until it runs out of steps."""
    config = types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=tools.schemas())],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
    )
    contents = [types.Content(role="user", parts=[types.Part(text=task)])]

    for _ in range(max_steps):
        response = generate(contents, config=config)
        call = find_function_call(response)
        if call is None:
            return response.text

        contents.append(response.candidates[0].content)
        result = tools.run(call.name, dict(call.args))
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_function_response(
                name=call.name, response={"result": result},
            )],
        ))
        return result

    return "Error: ran out of steps."
