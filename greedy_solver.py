"""Greedy solver: at each step, pick the map that covers the most frontier quests."""

from quest_list import Maps


def compute_frontier(completed: set[str], discovered: set[str], quest_list: dict) -> set[str]:
    """Return quests that are discovered, not completed, and have all prerequisites met."""
    frontier = set()
    for q in discovered:
        if q in completed:
            continue
        if q not in quest_list:
            continue
        prereqs = quest_list[q].get("prerequisites", [])
        if all(p in completed for p in prereqs):
            frontier.add(q)
    return frontier


def discover_new_quests(just_completed: set[str], completed: set[str], discovered: set[str], quest_list: dict) -> set[str]:
    """Given quests just completed this game, return newly discovered quest names."""
    newly_discovered = set()
    for q in just_completed:
        for nq in quest_list[q].get("new_quests", []):
            if nq not in discovered and nq not in completed:
                newly_discovered.add(nq)
    return newly_discovered


def greedy_solve(quest_list: dict, first_quests: list[str]) -> list[tuple[Maps, list[str]]]:
    """
    Run the greedy algorithm.

    Returns a list of (map, [quests_completed]) tuples representing each game.
    """
    completed: set[str] = set()
    discovered: set[str] = set(first_quests)
    all_quests = set(quest_list.keys())
    schedule: list[tuple[Maps, list[str]]] = []

    while completed != all_quests:
        frontier = compute_frontier(completed, discovered, quest_list)

        if not frontier:
            # Safety check: no quests available but not all done
            remaining = all_quests - completed
            print(f"WARNING: No quests in frontier but {len(remaining)} quests remain:")
            for q in sorted(remaining):
                prereqs = quest_list[q].get("prerequisites", [])
                unmet = [p for p in prereqs if p not in completed]
                in_disc = q in discovered
                print(f"  '{q}' - discovered={in_disc}, unmet_prereqs={unmet}")
            break

        # Score each map by how many frontier quests it covers
        best_map = None
        best_quests: list[str] = []
        best_count = -1

        for m in Maps:
            covered = [q for q in frontier if m in quest_list[q]["maps"]]
            if len(covered) > best_count:
                best_count = len(covered)
                best_map = m
                best_quests = covered

        if best_map is None or best_count == 0:
            # No map covers any frontier quest — should not happen if data is valid
            print("WARNING: No map covers any frontier quest.")
            break

        # Play this game
        just_completed = set(best_quests)
        completed |= just_completed
        schedule.append((best_map, sorted(best_quests)))

        # Discover new quests unlocked by what we just completed
        new_disc = discover_new_quests(just_completed, completed, discovered, quest_list)
        discovered |= new_disc

    return schedule


def _title_case(s: str) -> str:
    """Title-case a string without capitalizing after apostrophes."""
    return " ".join(
        word[0].upper() + word[1:] if word else word
        for word in s.split(" ")
    )


def format_schedule(schedule: list[tuple[Maps, list[str]]]) -> str:
    """Format a game schedule as a string."""
    lines = []
    lines.append(f"Total games: {len(schedule)}")
    lines.append("-" * 60)
    for i, (map_choice, quests) in enumerate(schedule, 1):
        lines.append(f"Game {i}: {map_choice.value}")
        for q in quests:
            lines.append(f"    \u2022 {_title_case(q)}")
    lines.append("-" * 60)
    return "\n".join(lines)


def print_schedule(schedule: list[tuple[Maps, list[str]]]) -> None:
    """Pretty-print a game schedule."""
    print(format_schedule(schedule))


if __name__ == "__main__":
    schedule = greedy_solve()
    print("=== GREEDY SOLVER RESULT ===")
    print_schedule(schedule)
