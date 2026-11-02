"""
Command line entry point.

    python -m agent.cli --task "A Scale plan costs 499 dollars a month. What would 6 months cost, minus a 150 dollar loyalty discount?"
    python -m agent.cli --task "..." --max-steps 5 --quiet
    python -m agent.cli --task "..." --plan
    python -m agent.cli --task "..." --session karen
    python -m agent.cli --task "..." --retrieve
    python -m agent.cli --task "..." --orchestrate
    python -m agent.cli --task "..." --team

DO NOT CHANGE THE INTERFACE. Later in the term you will run each other's
agents, and that only works if every agent is invoked the same way. Add
options if you like, but --task must keep working exactly as it does now.
"""

import argparse
import sys

from agent import delegate, loop, memory, planner, retrieval, team
from agent import sandbox  # noqa: F401  (adds run_python to the tools)


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
    parser.add_argument(
        "--session",
        help="remember this conversation under a name, across separate "
             "runs (Week 5)",
    )
    parser.add_argument(
        "--retrieve", action="store_true",
        help="fold in the most relevant documents from data/ before "
             "acting (Week 6), instead of relying on the model to call "
             "search_files/read_file itself",
    )
    parser.add_argument(
        "--orchestrate", action="store_true",
        help="split the task across sub-agents, each in its own fresh "
             "conversation, then combine their answers (Weeks 7-8)",
    )
    parser.add_argument(
        "--team", action="store_true",
        help="a researcher finds the answer and a checker verifies it, "
             "each with its own instructions and tools (Week 11)",
    )
    args = parser.parse_args(argv)

    if args.team:
        run_fn = team.team
    elif args.orchestrate:
        run_fn = delegate.orchestrate
    elif args.plan:
        run_fn = planner.run_with_plan
    else:
        run_fn = loop.run
    task = args.task

    try:
        if args.retrieve:
            task = retrieval.with_retrieval(task)

        if args.session:
            task = memory.with_memory(task, args.session)

        answer = run_fn(
            task,
            max_steps=args.max_steps,
            verbose=not args.quiet,
        )

        if args.session:
            memory.save(args.session, args.task, answer)
    except NotImplementedError:
        if args.team:
            what, where = "team", "agent/team.py"
        elif args.orchestrate:
            what, where = "orchestrator", "agent/delegate.py"
        elif args.retrieve:
            what, where = "retrieval", "agent/retrieval.py"
        elif args.session:
            what, where = "memory", "agent/memory.py"
        elif args.plan:
            what, where = "planner", "agent/planner.py"
        else:
            what, where = "loop", "agent/loop.py"
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
