"""
The tools your agent can use.

A tool is two things that have to stay in step:

  1. A normal Python function that does the work.
  2. A schema describing it, which is all the model ever sees.

The model cannot run your function. It reads the schema, decides whether the
tool is worth calling, and sends back a request naming the tool and its
arguments. Your loop runs the function and hands the result back.

So the description IS the interface. If it is vague, the model will call the
tool with the wrong arguments, and nothing will tell you that is what happened.

Adding a tool means three steps:
  1. Write the function.
  2. Write its schema.
  3. Add both to TOOLS at the bottom.
"""

# =====================================================================
# A worked example. Copy this shape.
# =====================================================================

def calculator(expression: str) -> str:
    """
    Evaluate a simple arithmetic expression.

    Note what this does NOT do: it does not run arbitrary Python. It allows
    digits and four operators and nothing else. That restriction is the whole
    reason this is safe to expose.

    In Week 7 you will give an agent a real code execution tool, and you will
    have to think much harder about this than you do here.
    """
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "Error: only digits and + - * / ( ) are allowed."
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"


CALCULATOR_SCHEMA = {
    "name": "calculator",
    "description": (
        "Evaluate a simple arithmetic expression and return the result. "
        "Use this for any calculation rather than working it out yourself."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": (
                    "An arithmetic expression using only digits and the "
                    "operators + - * / and parentheses. For example: (17*23)+4"
                ),
            }
        },
        "required": ["expression"],
    },
}


# =====================================================================
# YOUR TURN
# =====================================================================
# Port your Week 2 classifier in here as a second tool.
#
#   1. Copy your best prompt across from week 2.
#   2. Write classify_ticket(text) so it returns a category string.
#   3. Write CLASSIFY_SCHEMA to describe it.
#   4. Add both to TOOLS below.
#
# Two things worth thinking about while you do it:
#
#   - Your Week 2 function had to parse JSON out of a text reply. Does it
#     still need to, now that the schema constrains the output? What is the
#     tool actually returning to the loop?
#
#   - What should the description say? The model decides whether to call this
#     based on nothing but those words. Write it, then look at what the model
#     actually does with it.

# def classify_ticket(text: str) -> str:
#     ...
#
# CLASSIFY_SCHEMA = {
#     ...
# }


# =====================================================================
# The registry. The loop uses this to find and run tools.
# =====================================================================
#
# name -> (python function, schema)
#
TOOLS = {
    "calculator": (calculator, CALCULATOR_SCHEMA),
    # "classify_ticket": (classify_ticket, CLASSIFY_SCHEMA),
}


def schemas():
    """Every schema, in the shape the API wants for its tools parameter."""
    return [schema for _fn, schema in TOOLS.values()]


def run(name: str, args: dict) -> str:
    """
    Run the tool the model asked for.

    Returns a string either way. If the tool fails, the error message IS the
    result, and it goes back to the model. That is deliberate. A model that
    is told what went wrong can often recover; a crashed program cannot.
    """
    if name not in TOOLS:
        return f"Error: there is no tool called {name}."
    fn, _schema = TOOLS[name]
    try:
        return str(fn(**args))
    except Exception as e:
        return f"Error running {name}: {type(e).__name__}: {e}"
