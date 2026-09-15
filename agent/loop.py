"""
The agent loop.

THIS FILE IS THE LAB. Everything else in the repo already works.

You are writing about fifteen lines. They are the same four boxes you drew
on the board in Week 1:

    OBSERVE   everything that has happened so far
    THINK     the model decides what to do next
    ACT       your code runs it and gets a result
    DONE?     or go round again

The model does exactly one of those. The rest is you.
"""

from google.genai import types

from agent import tools
from agent.llm import generate

MAX_STEPS = 10


def find_function_call(response):
    """
    Pull the tool request out of a reply, if there is one.

    A reply is made of parts. Usually one, but a model can return text AND a
    tool request in the same reply, so we look through all of them.

    Returns the function call, or None if the model answered in words instead.
    Written for you, because the shape of a response is API trivia and not the
    point of this lab.
    """
    candidate = response.candidates[0]
    for part in candidate.content.parts:
        if getattr(part, "function_call", None):
            return part.function_call
    return None


def run(task: str, max_steps: int = MAX_STEPS, verbose: bool = True) -> str:
    """
    Run the agent until it answers, or until it has had enough turns.

    Args:
        task:       what the user wants, in plain language
        max_steps:  how many times round the loop before giving up
        verbose:    print each step, so you can see what it is doing

    Returns:
        The agent's final answer, as a string.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  Set up the config with your tools attached.

            config = types.GenerateContentConfig(
                tools=[types.Tool(function_declarations=tools.schemas())],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                ),
            )

        That second argument turns OFF the SDK's own loop. You are writing
        the loop. If you let the SDK do it, you will not be able to see or
        debug any of this, which is the entire point of the exercise.

    2.  Start the conversation with the task.

            contents = [types.Content(role="user",
                                      parts=[types.Part(text=task)])]

    3.  Loop, up to max_steps times. Each time round:

        a.  Call the model with everything so far.
                response = generate(contents, config=config)

        b.  Look for a tool request.
                call = find_function_call(response)

        c.  If there is no tool request, the model has answered.
            Return response.text.

        d.  Otherwise, run the tool.
                result = tools.run(call.name, dict(call.args))

        e.  Append TWO things to contents: what the model said, and what
            the tool returned. Both, in that order. If you skip the first,
            the transcript stops making sense and the model gets confused
            about what it already asked for.

                contents.append(response.candidates[0].content)
                contents.append(types.Content(
                    role="user",
                    parts=[types.Part.from_function_response(
                        name=call.name,
                        response={"result": result},
                    )],
                ))

    4.  If the loop finishes without the model ever answering, say so.
        Do not return None. Something that ran out of steps and something
        that finished are different, and the caller needs to know which.

    ------------------------------------------------------------------
    WHILE YOU WRITE IT
    ------------------------------------------------------------------

    Print something each time round when verbose is True. You cannot debug
    an agent you cannot see. At minimum: the step number, the tool it asked
    for, and what came back.

    Every step resends the whole conversation. Watch the input token count
    grow. That is Week 5 arriving early.
    """
    raise NotImplementedError("write the loop")


if __name__ == "__main__":
    # A task that needs the calculator, so you can tell whether the loop works.
    print(run("A Scale plan costs 499 dollars a month. What would 6 months cost, minus a 150 dollar loyalty discount?"))
