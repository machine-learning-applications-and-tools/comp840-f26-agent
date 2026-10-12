"""
Week 7 demo · What "sandboxed" actually buys you

Three short demonstrations, none of them touching the real API:

  1. A naive run_python(), bare exec() in this process, can read
     anything this process can read. That includes environment
     variables, which is where GEMINI_API_KEY lives.
  2. The same code, run as a separate process, still sees the
     environment by default. Being a subprocess does not hide it.
  3. Stripping the child's environment (MINIMAL_ENV) is what hides it.
     That one argument is the difference between a separate process
     and a contained one.

DEMO_SECRET below is a fake value made only for this demo. It is not
your real API key. The demo does not import agent.tools, so you see the
naive version fail before you write the guarded one.

Run:  python demo_sandbox.py
Costs 0 API calls.
"""

import os
import subprocess
import sys

LINE = "-" * 66

os.environ["DEMO_SECRET"] = "do-not-leak-me"

# An empty environment, except that Windows needs SYSTEMROOT for Python to
# start at all. It only says where Windows is installed. On Mac this is {}.
MINIMAL_ENV = (
    {"SYSTEMROOT": os.environ["SYSTEMROOT"]} if sys.platform == "win32" else {}
)
CODE = "import os; print(os.environ.get('DEMO_SECRET'))"

print(LINE)
print("1. A naive run_python(): bare exec(), in this process\n")
print(f"    code:  {CODE!r}")

exec_globals = {}
exec(CODE, exec_globals)
print("\n    That printed the real DEMO_SECRET value. exec() runs with this")
print("    process's own environment and file access. There is no boundary")
print("    at all between the code and the agent running it.")

print("\n" + LINE)
print("2. The same code, as a separate process\n")

result = subprocess.run(
    [sys.executable, "-c", CODE], capture_output=True, text=True
)
print(f"    stdout: {result.stdout.strip()!r}")
print("\n    Still leaked. A separate process is not a contained one.")
print("    By default a child process inherits this process's whole")
print("    environment, secrets included.")

print("\n" + LINE)
input("Press Enter to run part 3...")

print("\n" + LINE)
print("3. The same code, with the child's environment stripped\n")

result = subprocess.run(
    [sys.executable, "-c", CODE],
    capture_output=True, text=True,
    env=MINIMAL_ENV,
)
print(f"    stdout: {result.stdout.strip()!r}")
print("\n    env=MINIMAL_ENV replaces the child's environment instead of")
print("    inheriting it. On Windows it keeps only SYSTEMROOT, so Python can start.")
print("    That one argument to subprocess.run() is what hides the API key.")

print("\n" + LINE)
print("What this does NOT show: a timeout")
print("""
subprocess.run(..., timeout=N) kills a hung child process, on Windows
and Mac. run_python(), which you write this week, uses that argument.

None of this makes run_python() fully safe. The child process above
still has full access to your files and the network. Stripping the
environment closes one gap, not all of them. Say that plainly rather
than calling it "sandboxed."
""")
