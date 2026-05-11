"""Main entry point: validate data, run greedy solver, run ILP solver, compare."""

import argparse
import json
import os
import sys

from validate import validate
from greedy_solver import greedy_solve, print_schedule as print_greedy, format_schedule as format_greedy
from ilp_solver import ilp_solve, print_schedule as print_ilp, format_schedule as format_ilp
from quest_list import Maps

_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(_DIR, "results.txt")
BEST_SCHEDULE_FILE = os.path.join(_DIR, "best_schedule.json")


def _save_schedule(schedule: list[tuple[Maps, list[str]]], path: str) -> None:
    """Persist a schedule to JSON so the next run can resume from it."""
    data = [(m.value, quests) for m, quests in schedule]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _load_schedule(path: str) -> list[tuple[Maps, list[str]]] | None:
    """Load a previously saved schedule, or return None."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        map_lookup = {m.value: m for m in Maps}
        return [(map_lookup[m_name], quests) for m_name, quests in data]
    except Exception as e:
        print(f"  Warning: could not load {path}: {e}")
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Arc Raiders quest optimizer")
    parser.add_argument(
        "--bp", action="store_true",
        help="Use bp_quest_list instead of quest_list",
    )
    parser.add_argument(
        "--minutes",
        type=float,
        default=30,
        help="Solver time limit in minutes (default: 30)",
    )
    args = parser.parse_args()
    time_limit = int(args.minutes * 60)

    # Import the appropriate quest data
    if args.bp:
        from bp_quest_list import quest_list as ql, FIRST_QUESTS
        label = "bp_quest_list"
    else:
        from quest_list import quest_list as ql, FIRST_QUESTS
        label = "quest_list"

    # Use label-specific filenames so results don't overwrite each other
    results_file = os.path.join(_DIR, f"results_{label}.txt") if args.bp else RESULTS_FILE
    schedule_file = os.path.join(_DIR, f"best_schedule_{label}.json") if args.bp else BEST_SCHEDULE_FILE

    print(f"Using quest data from: {label}")
    print()

    # Step 1: Validate quest data
    print("=" * 60)
    print("STEP 1: VALIDATING QUEST DATA")
    print("=" * 60)
    if not validate(ql, FIRST_QUESTS):
        print("\nAborting: fix validation errors before running solvers.")
        sys.exit(1)

    # Step 2: Run greedy solver
    print()
    print("=" * 60)
    print("STEP 2: GREEDY SOLVER")
    print("=" * 60)
    greedy_schedule = greedy_solve(ql, FIRST_QUESTS)
    print(format_greedy(greedy_schedule))
    greedy_count = len(greedy_schedule)

    # Load previous best schedule if it exists (to resume from last run)
    prev_best = _load_schedule(schedule_file)
    if prev_best is not None:
        print(f"\nLoaded previous best: {len(prev_best)} games from {schedule_file}")

    # Pick the better warm-start: previous best or greedy (ignore empty schedules)
    if prev_best is not None and len(prev_best) > 0 and len(prev_best) <= greedy_count:
        warm_start = prev_best
        print(f"Using previous best ({len(prev_best)} games) as warm-start")
    else:
        warm_start = greedy_schedule
        print(f"Using greedy ({greedy_count} games) as warm-start")

    # Step 3: Run ILP solver
    print()
    print("=" * 60)
    print("STEP 3: ILP OPTIMAL SOLVER")
    print("=" * 60)
    ilp_schedule = ilp_solve(
        ql,
        FIRST_QUESTS,
        t_max=len(warm_start),
        warm_start=warm_start,
        time_limit=time_limit,
    )

    if ilp_schedule is not None:
        print()
        print(format_ilp(ilp_schedule))
        ilp_count = len(ilp_schedule)
    else:
        print("ILP solver failed to find a solution.")
        ilp_count = None

    # Step 4: Compare results and determine overall best
    print()
    print("=" * 60)
    print("COMPARISON")
    print("=" * 60)
    print(f"  Greedy:        {greedy_count} games")
    if prev_best is not None:
        print(f"  Previous best: {len(prev_best)} games")
    if ilp_count is not None:
        print(f"  ILP (this run): {ilp_count} games")
    else:
        print("  ILP (this run): failed")

    # Determine the overall best schedule across all sources
    candidates: list[tuple[str, list[tuple[Maps, list[str]]]]] = [
        ("Greedy", greedy_schedule),
    ]
    if prev_best is not None:
        candidates.append(("Previous best", prev_best))
    if ilp_schedule is not None:
        candidates.append(("ILP", ilp_schedule))

    best_label, best_schedule = min(candidates, key=lambda x: len(x[1]))
    best_count = len(best_schedule)
    print(f"\n  >>> Best overall: {best_count} games ({best_label}) <<<")

    # Save the best schedule for next run to resume from
    _save_schedule(best_schedule, schedule_file)
    print(f"  Saved to {schedule_file} for next run")

    # Write human-readable results
    best_text = format_ilp(best_schedule)
    with open(results_file, "w", encoding="utf-8") as f:
        f.write(f"Best schedule ({best_label}, {best_count} games):\n")
        f.write(best_text + "\n")
    print(f"  Written to {results_file}")


if __name__ == "__main__":
    main()
