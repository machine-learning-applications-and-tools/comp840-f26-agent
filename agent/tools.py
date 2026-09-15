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

from pathlib import Path

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
# New this week: eyes on files. Three tools, one shape, one guard.
# =====================================================================
#
# The model never sees a real filesystem path. It only ever sees names, and
# every name it sends back has to be checked before anything touches disk.

DATA_DIR = (Path(__file__).parent.parent / "data").resolve()


def _safe_path(name: str) -> Path:
    """
    Resolve `name` to a path inside data/, or raise ValueError.

    Three attacks, two checks:

      ../ traversal    climbing out of data/ with a relative path, e.g.
                        "../../etc/passwd"
      absolute paths   "/etc/passwd", ignoring data/ entirely -- pathlib's
                        `/` operator silently discards the left side when
                        you join an absolute path onto it, so joining
                        alone does not stop this the way you'd expect
      symlinks         a link sitting inside data/ that points somewhere
                        else -- .resolve() follows it before the
                        containment check below ever runs, so the check
                        still catches where it actually points

    Reject absolute paths first, since joining can't. Then resolve ".."
    and symlinks and confirm what's left is still inside DATA_DIR -- that
    second check is what catches both traversal and symlinks, in one move.
    """
    if Path(name).is_absolute():
        raise ValueError(f"{name!r} is an absolute path.")
    candidate = (DATA_DIR / name).resolve()
    if not candidate.is_relative_to(DATA_DIR):
        raise ValueError(f"{name!r} resolves outside data/.")
    return candidate


def _iter_data_files():
    """Every real file in data/, each re-checked through the same guard the
    model's own requests go through. A symlink inside data/ that points
    outside it should not be listed, read, or searched either."""
    for entry in sorted(DATA_DIR.iterdir()):
        try:
            path = _safe_path(entry.name)
        except ValueError:
            continue
        if path.is_file():
            yield path


def list_files() -> str:
    """Return the names of every file in data/, one per line, nothing else."""
    return "\n".join(path.name for path in _iter_data_files())


LIST_FILES_SCHEMA = {
    "name": "list_files",
    "description": (
        "List the names of every file in data/. Call this first if you "
        "don't already know what's there."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def read_file(name: str) -> str:
    """Return the contents of one file in data/."""
    try:
        path = _safe_path(name)
    except ValueError as e:
        return f"Error: {e}"
    if not path.is_file():
        return f"Error: no file called {name!r} in data/."
    return path.read_text(encoding="utf-8")


READ_FILE_SCHEMA = {
    "name": "read_file",
    "description": (
        "Return the full contents of one file in data/. Use list_files "
        "first if you don't already know the exact filename."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": (
                    "Exact filename inside data/, e.g. ticket_014.txt. "
                    "No paths, no directories."
                ),
            }
        },
        "required": ["name"],
    },
}


def search_files(query: str) -> str:
    """
    Plain substring search across every file in data/.

    Returns one line per match, formatted as "filename: matching line". Not
    a regex, not case-insensitive, just `in`. That is enough to be useful
    and simple enough that what it does is never a mystery.
    """
    hits = []
    for path in _iter_data_files():
        for line in path.read_text(encoding="utf-8").splitlines():
            if query in line:
                hits.append(f"{path.name}: {line.strip()}")
    if not hits:
        return f"No matches for {query!r}."
    return "\n".join(hits)


SEARCH_FILES_SCHEMA = {
    "name": "search_files",
    "description": (
        "Search every file in data/ for a plain substring and return each "
        "match as 'filename: matching line'. Case-sensitive, not a regex. "
        "Use this to find which file has what you need before calling "
        "read_file, rather than reading files one by one."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Plain text to search for. Not a regex.",
            }
        },
        "required": ["query"],
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
    "list_files": (list_files, LIST_FILES_SCHEMA),
    "read_file": (read_file, READ_FILE_SCHEMA),
    "search_files": (search_files, SEARCH_FILES_SCHEMA),
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
