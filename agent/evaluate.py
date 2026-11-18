"""
Evaluation. This file is the lab.

Run every case in eval_cases.py, check each run two ways, and report what
it cost:

    outcome      is the final answer right?
    trajectory   did it read the right files, use the right tools, and stay
                 under the tool-call limit?

Try it once check_trajectory() and evaluate() work:

    python -m agent.evaluate --cases 1 3
    python -m agent.evaluate
    python -m agent.evaluate --strategy team
"""

import argparse
import re
import sys
import time

from agent import llm, loop, tools
from eval_cases import CASES


# =======================================================================
# GIVEN. Read these, do not change them.
# =======================================================================

_NUMBER = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?")


def numbers_in(text: str) -> list[float]:
    """
    Every number written in `text`, as floats.

    "$4,200 a year, or 66.67%" -> [4200.0, 66.67]

    Given. Commas are removed and units are ignored, so "$350" and
    "350 dollars" both come back as 350.0.
    """
    return [float(m.replace(",", "")) for m in _NUMBER.findall(text or "")]


def record(task: str, run_fn=None, max_steps: int = loop.MAX_STEPS) -> dict:
    """
    Run the agent on `task` once, and record everything about the run.

    Given. Returns a TRACE, a dict with:

        task          the task text
        answer        the final answer string
        steps         every tool call, in order, each as
                      {"tool": name, "args": {...}, "result": "..."}
        calls         generate() calls the run made
        input_tokens  input tokens across those calls
        total_tokens  input plus output tokens
        seconds       wall-clock time, most of it rate-limit pacing

    To see each tool call without changing loop.py, it swaps tools.run for
    a wrapper that writes the call down and then runs the real tool. The
    real tools.run is put back at the end.

    run_fn is whatever runs the agent: loop.run (the default),
    planner.run_with_plan, delegate.orchestrate, or team.team. All four
    take the same arguments.
    """
    run_fn = run_fn or loop.run
    steps = []
    real_run = tools.run

    def recording_run(name, args):
        result = real_run(name, args)
        steps.append({"tool": name, "args": dict(args), "result": str(result)})
        return result

    before = dict(llm.stats)
    start = time.monotonic()
    tools.run = recording_run
    try:
        answer = run_fn(task, max_steps=max_steps, verbose=False)
    finally:
        tools.run = real_run

    return {
        "task": task,
        "answer": answer or "",
        "steps": steps,
        "calls": llm.stats["calls"] - before["calls"],
        "input_tokens": llm.stats["input_tokens"] - before["input_tokens"],
        "total_tokens": llm.stats["output_tokens"] - before["output_tokens"],
        "seconds": time.monotonic() - start,
    }


def print_report(rows: list[dict]) -> None:
    """
    Print one line per case, the failed checks under it, then the totals.

    Given. `rows` is what evaluate() returns.
    """
    print("\n" + "-" * 66)
    for row in rows:
        out, traj, tr = row["outcome"], row["trajectory"], row["trace"]
        print(
            f"case {row['case']}   "
            f"outcome {sum(out.values())}/{len(out)}   "
            f"trajectory {sum(traj.values())}/{len(traj)}   "
            f"{tr['calls']} calls   {tr['total_tokens']:,} tokens   "
            f"{tr['seconds']:.0f}s"
        )
        for name, ok in list(out.items()) + list(traj.items()):
            if not ok:
                print(f"    FAILED  {name}")

    n = len(rows)
    calls = sum(r["trace"]["calls"] for r in rows)
    tokens = sum(r["trace"]["total_tokens"] for r in rows)
    seconds = sum(r["trace"]["seconds"] for r in rows)
    out_ok = sum(all(r["outcome"].values()) for r in rows)
    traj_ok = sum(all(r["trajectory"].values()) for r in rows)
    print("-" * 66)
    print(f"outcome passed      {out_ok}/{n} cases")
    print(f"trajectory passed   {traj_ok}/{n} cases")
    print(f"cost                {calls} calls, {tokens:,} tokens, {seconds:.0f}s")
    if calls:
        print(f"                    500 calls a day buys about "
              f"{500 // calls} full runs like this one")


def check_outcome(trace: dict, case: dict) -> dict:
    """
    Is the final answer right? Returns one named check per thing that
    must be true, each True or False.

    Given. Read it before you write check_trajectory(), which returns the
    same shape. For example, for case 1:

        {"finished": True,
         "answer contains 350": True,
         "answer contains 4200": False}

    "finished" fails when the run ran out of steps. loop.run() then returns
    a string starting "Error: gave up".

    Each expected number passes if ANY number in the answer is within its
    tolerance. Cases 2, 4 and 5 have no numbers, so they only get
    "finished".
    """
    answer = trace["answer"]
    checks = {"finished": not answer.startswith("Error: gave up")}
    found = numbers_in(answer)
    for value, tol in case["numbers"]:
        checks[f"answer contains {value:g}"] = any(
            abs(n - value) <= tol for n in found
        )
    return checks


# =======================================================================
# WHAT YOU HAVE TO WRITE. The core lab, required for everyone.
# =======================================================================

def check_trajectory(trace: dict, case: dict) -> dict:
    """
    Did the run get there sensibly? Return one named check per
    expectation, each True or False.

    For example, for case 0:

        {"read ticket_009.txt": True,
         "read product_notes_billing.txt": False,
         "used calculator or run_python": True,
         "at most 8 tool calls": True,
         "no tool errors": True}

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    trace["steps"] is a list like
        [{"tool": "read_file", "args": {"name": "pricing.txt"}, "result": "..."}, ...]

    1.  Collect two sets from the steps: the file names passed to
        read_file (s["args"].get("name")), and the names of every tool
        used at all.

    2.  For each group in case["must_read"], one check named
        "read " + " or ".join(sorted(group)). It passes if the agent read
        ANY file in the group:  bool(group & files_read)

    3.  For each group in case["must_use"], one check named
        "used " + " or ".join(sorted(group)), the same way, against the
        tools used.

    4.  f"at most {case['max_tool_calls']} tool calls": the number of
        steps is no more than case["max_tool_calls"].

    5.  "no tool errors": no step's result starts with "Error". tools.run()
        returns errors as strings, not exceptions.
    """
    raise NotImplementedError("write check_trajectory")


def evaluate(cases: list, run_fn=None) -> list[dict]:
    """
    Run every case once, check it both ways, and return one row per case.

    `cases` is a list of (number, case) pairs, such as
    [(1, CASES[1]), (5, CASES[5])], so each row can say which case it is.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    For each (i, case) in cases:

    1.  Print a progress line, such as f"running case {i} ...". Runs are
        slow because of the rate limit.

    2.  trace = record(case["task"], run_fn)

    3.  Append a row:

            {"case": i,
             "trace": trace,
             "outcome": check_outcome(trace, case),
             "trajectory": check_trajectory(trace, case)}

    Return the list of rows. print_report(), given above, prints them.
    """
    raise NotImplementedError("write evaluate")


# =======================================================================
# BENCHMARK. Part of the lab, required for everyone.
#
# Run the same cases with every strategy you have built, and compare the
# results side by side.
# =======================================================================

STRATEGIES = ["loop", "plan", "orchestrate", "team"]


def benchmark(cases: list, strategies=STRATEGIES) -> list[dict]:
    """
    Evaluate the same cases with each strategy, and print one line per
    strategy.

    ------------------------------------------------------------------
    WHAT YOU HAVE TO WRITE
    ------------------------------------------------------------------

    For each strategy name in `strategies`:

    1.  rows = evaluate(cases, _run_fn(name))

        If that strategy's lab from an earlier week is not finished, it
        raises NotImplementedError. Catch it, print that the strategy was
        skipped, and go on to the next one.

    2.  Summarize the rows into one dict:

            {"strategy": name,
             "outcome": cases where every outcome check passed,
             "trajectory": cases where every trajectory check passed,
             "cases": len(rows),
             "calls": total calls,
             "tokens": total tokens,
             "seconds": total seconds}

        The totals come from row["trace"], the same fields
        print_report() adds up.

    3.  When every strategy is done, print one line per summary, for
        example:

            loop          outcome 2/2   trajectory 1/2    9 calls   ...
            team          outcome 2/2   trajectory 2/2   14 calls   ...

    Return the list of summaries.

    Run it on two cases first. Every strategy runs every case, so this
    costs four times one evaluation:

        python -m agent.evaluate --cases 1 3 --benchmark
    """
    raise NotImplementedError("write benchmark")


# =======================================================================
# Command line. Given.
# =======================================================================

def _run_fn(strategy):
    if strategy == "plan":
        from agent import planner
        return planner.run_with_plan
    if strategy == "orchestrate":
        from agent import delegate
        return delegate.orchestrate
    if strategy == "team":
        from agent import team
        return team.team
    return loop.run


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m agent.evaluate",
        description="Run the evaluation cases and report outcome, "
                    "trajectory and cost.",
    )
    parser.add_argument("--cases", type=int, nargs="+",
                        help="which cases to run, by number (default: all)")
    parser.add_argument("--strategy", choices=STRATEGIES,
                        default="loop", help="how to run the agent")
    parser.add_argument("--benchmark", action="store_true",
                        help="run the cases with every strategy and compare "
                             "them")
    parser.add_argument("--trace", action="store_true",
                        help="print every tool call of every run")
    args = parser.parse_args(argv)

    try:
        numbers = args.cases if args.cases else range(len(CASES))
        cases = [(i, CASES[i]) for i in numbers]
        if args.benchmark:
            benchmark(cases)
            llm.report()
            return 0
        rows = evaluate(cases, _run_fn(args.strategy))

        if args.trace:
            for row in rows:
                print(f"\ncase {row['case']}: {row['trace']['answer'][:200]}")
                for s in row["trace"]["steps"]:
                    print(f"    {s['tool']}({s['args']})")

        print_report(rows)
    except NotImplementedError as e:
        print(f"Not written yet: {e}. That is this week's lab, in "
              f"agent/evaluate.py.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nstopped", file=sys.stderr)
        return 130

    llm.report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
