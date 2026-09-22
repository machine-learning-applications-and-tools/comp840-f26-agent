"""
Command line entry point.

    python -m agent.cli --task "A Scale plan costs 499 dollars a month. What would 6 months cost, minus a 150 dollar loyalty discount?"
    python -m agent.cli --task "..." --max-steps 5 --quiet
    python -m agent.cli --task "..." --plan

DO NOT CHANGE THE INTERFACE. Later in the term you will run each other's
agents, and that only works if every agent is invoked the same way. Add
options if you like, but --task must keep working exactly as it does now.
"""

import argparse
import sys

from agent import loop, planner


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="agent",
        description="Run the agent on a task.",
    )
    parser.add_argument(
        "--task", required=True,
        help="what you want the agent to do, in plain language",
    )
    parser.add_argument(
        "--max-steps", type=int, default=loop.MAX_STEPS,
        help=f"how many times round the loop before giving up "
             f"(default {loop.MAX_STEPS})",
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="only print the final answer, not each step",
    )
    parser.add_argument(
        "--plan", action="store_true",
        help="write a numbered plan before acting (Week 4), instead of "
             "reacting one step at a time",
    )
    args = parser.parse_args(argv)

    run_fn = planner.run_with_plan if args.plan else loop.run

    try:
        answer = run_fn(
            args.task,
            max_steps=args.max_steps,
            verbose=not args.quiet,
        )
    except NotImplementedError:
        what = "planner" if args.plan else "loop"
        where = "agent/planner.py" if args.plan else "agent/loop.py"
        print(f"The {what} is not written yet. That is this week's lab: "
              f"fill in {where}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nstopped", file=sys.stderr)
        return 130

    if not args.quiet:
        print("\n" + "-" * 60)
    print(answer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
