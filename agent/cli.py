"""
Command line entry point.

    python -m agent.cli --task "A Scale plan costs 499 dollars a month. What would 6 months cost, minus a 150 dollar loyalty discount?"
    python -m agent.cli --task "..." --max-steps 5 --quiet

DO NOT CHANGE THE INTERFACE. Later in the term you will run each other's
agents, and that only works if every agent is invoked the same way. Add
options if you like, but --task must keep working exactly as it does now.
"""

import argparse
import sys

from agent import loop


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
    args = parser.parse_args(argv)

    try:
        answer = loop.run(
            args.task,
            max_steps=args.max_steps,
            verbose=not args.quiet,
        )
    except NotImplementedError:
        print("The loop is not written yet. That is this week's lab: "
              "fill in run() in agent/loop.py", file=sys.stderr)
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
