"""
A tool that can go wrong.

THIS FILE IS PART OF THIS WEEK'S LAB (Tuesday). The other part is
delegate.py (Wednesday).

Every tool so far is safe by CONSTRUCTION: calculator only accepts four
operators, the file tools can only reach inside data/. run_python cannot
be made safe that way, because its purpose is running code you did not
write in advance. Its safety has to come from where it runs, not from
checking its text.

Two functions below are required for everyone. run_python() stops code
that never finishes. run_python_contained() also hides your API key from
the code. Neither one makes running code fully safe.

This file is separate from tools.py on purpose: tools.py holds your own
work from Week 3, including your classifier, so this week does not touch
it. The last lines of this file add run_python to the same TOOLS registry
the loop already reads. The loop never needs to know.
"""

import os
import subprocess
import sys

RUN_PYTHON_TIMEOUT = 5
RUN_PYTHON_MAX_OUTPUT = 2000


def _truncate(text: str) -> str:
    """
    Given. Keep only the LAST RUN_PYTHON_MAX_OUTPUT characters.

    The last part, not the first, because a traceback ends with the error
    type and message. The cap also stops a script that prints a huge
    amount of output from flooding the loop.
    """
    return text[-RUN_PYTHON_MAX_OUTPUT:]


def run_python(code: str) -> str:
    """
    Run `code` as a completely separate Python process, not inside this
    one, and return what it printed.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    1.  Run it with subprocess.run(), not exec() in this process.
        sys.executable is the Python you are running now, and "-c"
        tells it to run the string that follows as code:

            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True, text=True,
                timeout=RUN_PYTHON_TIMEOUT,
            )

        This is why it has to be a separate process: when the time runs
        out, the operating system kills the child process. Code stuck in
        a loop inside this process could not be stopped that way.

    2.  When the time runs out, subprocess.run() raises
        subprocess.TimeoutExpired. Catch it and return
        f"Error: timed out after {RUN_PYTHON_TIMEOUT}s".

    3.  If result.returncode is 0, return _truncate(result.stdout).
        Otherwise return _truncate("Error: " + result.stderr).
    """
    raise NotImplementedError("write run_python")


RUN_PYTHON_SCHEMA = {
    "name": "run_python",
    "description": (
        "Run a short Python snippet and return what it printed to "
        "stdout. Use this for anything the calculator cannot do, such "
        "as loops, conditionals, or working with lists or strings. The code "
        "runs in a separate process with a "
        f"{RUN_PYTHON_TIMEOUT}-second time limit; anything still running "
        "after that is killed and reported as a timeout, not a crash."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": (
                    "A complete, self-contained Python script. It must "
                    "print() whatever it wants returned. There is no "
                    "separate return value, only what reaches stdout."
                ),
            }
        },
        "required": ["code"],
    },
}


# =====================================================================
# Required, the same as run_python() above.
#
# run_python() stops a HANG. It does nothing about what the code can
# still DO while it runs. A new process gets a copy of this process's
# environment variables, including GEMINI_API_KEY. This function hides
# them. It does not stop the code reading or deleting your files, or
# using the network. Say that honestly in week07-08-OUTPUT.md rather
# than calling it "sandboxed."
# =====================================================================

def _minimal_env() -> dict:
    """
    Given, not a stub. An environment with nothing in it except what
    Python itself needs to start.

    On Windows, Python cannot start with a completely empty environment:
    it needs SYSTEMROOT, which only says where Windows is installed.
    Without it the child dies with "Fatal Python error: ... failed to get
    random numbers" before running any of your code. So on Windows this
    keeps that one variable. On Mac and Linux it is just {}.

    Either way, GEMINI_API_KEY and everything else in os.environ is left
    out, which is the point.
    """
    if sys.platform == "win32":
        return {"SYSTEMROOT": os.environ["SYSTEMROOT"]}
    return {}


def run_python_contained(code: str) -> str:
    """
    run_python(), but the child process cannot see your environment
    variables. How long it can run is unchanged.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    Everything run_python() does, with one more argument to
    subprocess.run(). env= replaces the child's environment instead of
    copying this one. _minimal_env(), just above, is given:

        subprocess.run(..., env=_minimal_env())

    Check both functions with python -m agent.sandbox (the given block
    at the bottom of this file), and paste the output into
    week07-08-OUTPUT.md.
    """
    raise NotImplementedError("write run_python_contained")


# =====================================================================
# Registration. Given, not a stub.
#
# Adds run_python to the registry in tools.py, the same table calculator
# and the file tools live in. loop.run() asks tools.schemas() for the list
# every time it starts, so the model sees the new tool without loop.py
# changing at all. cli.py imports this file, which is what runs these
# lines.
# =====================================================================

from agent import tools  # noqa: E402

tools.TOOLS["run_python"] = (run_python, RUN_PYTHON_SCHEMA)


# =====================================================================
# Given. Run this file to check both functions without the agent:
#
#     python -m agent.sandbox
#
# 0 API calls. DEMO_SECRET is a fake value, not your real API key.
# =====================================================================

if __name__ == "__main__":
    os.environ["DEMO_SECRET"] = "leaked-if-you-see-this"
    snippet = "import os; print(os.environ.get('DEMO_SECRET'))"
    print("run_python:          ", run_python(snippet).strip())
    print("run_python_contained:", run_python_contained(snippet).strip())
