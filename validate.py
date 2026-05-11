"""Validate the quest_list data for consistency and reachability."""

import sys
from collections import deque

from quest_list import Maps


def validate(quest_list: dict, first_quests: list[str]) -> bool:
    """Run all validation checks. Returns True if valid, False otherwise."""
    errors: list[str] = []
    warnings: list[str] = []

    all_quest_names = set(quest_list.keys())

    # --- Check FIRST_QUESTS exist ---
    for fq in first_quests:
        if fq not in all_quest_names:
            errors.append(f"FIRST_QUESTS references unknown quest: '{fq}'")

    # --- Check all new_quests references exist ---
    for quest_name, data in quest_list.items():
        for nq in data.get("new_quests", []):
            if nq not in all_quest_names:
                errors.append(f"Quest '{quest_name}' has new_quest '{nq}' which doesn't exist")

    # --- Check all prerequisites references exist ---
    for quest_name, data in quest_list.items():
        for prereq in data.get("prerequisites", []):
            if prereq not in all_quest_names:
                errors.append(f"Quest '{quest_name}' has prerequisite '{prereq}' which doesn't exist")

    # --- Check every quest has 'maps' and 'new_quests' ---
    for quest_name, data in quest_list.items():
        if "maps" not in data or not data["maps"]:
            errors.append(f"Quest '{quest_name}' is missing 'maps' or has empty maps list")
        if "new_quests" not in data:
            errors.append(f"Quest '{quest_name}' is missing 'new_quests' field")

    # --- Check all maps are valid Maps enum values ---
    for quest_name, data in quest_list.items():
        for m in data.get("maps", []):
            if not isinstance(m, Maps):
                errors.append(f"Quest '{quest_name}' has invalid map value: {m}")

    # --- Check reachability via BFS from FIRST_QUESTS ---
    # A quest is "discoverable" if it's in FIRST_QUESTS or appears in
    # some discoverable quest's new_quests list.
    discovered = set(first_quests)
    queue = deque(first_quests)
    while queue:
        current = queue.popleft()
        if current not in all_quest_names:
            continue
        for nq in quest_list[current].get("new_quests", []):
            if nq not in discovered:
                discovered.add(nq)
                queue.append(nq)

    unreachable = all_quest_names - discovered
    for quest_name in sorted(unreachable):
        errors.append(f"Quest '{quest_name}' is not reachable from FIRST_QUESTS")

    # --- Check for quests with prerequisites that are never discovered ---
    for quest_name, data in quest_list.items():
        for prereq in data.get("prerequisites", []):
            if prereq in all_quest_names and prereq not in discovered:
                warnings.append(
                    f"Quest '{quest_name}' has prerequisite '{prereq}' which is unreachable"
                )

    # --- Print results ---
    if errors:
        print("=== VALIDATION ERRORS ===")
        for e in errors:
            print(f"  ✗ {e}")
        print()

    if warnings:
        print("=== WARNINGS ===")
        for w in warnings:
            print(f"  ⚠ {w}")
        print()

    # --- Print summary ---
    print("=== QUEST DATA SUMMARY ===")
    print(f"  Total quests: {len(all_quest_names)}")
    print(f"  Starting quests: {first_quests}")
    print(f"  Quests with prerequisites: {sum(1 for d in quest_list.values() if d.get('prerequisites'))}")
    print()

    # Per-map quest counts
    map_counts: dict[Maps, int] = {m: 0 for m in Maps}
    for data in quest_list.values():
        for m in data.get("maps", []):
            map_counts[m] += 1
    print("  Quests per map:")
    for m in Maps:
        print(f"    {m.value}: {map_counts[m]}")
    print()

    # Leaf quests (no new_quests and no prerequisites-gated children)
    leaf_quests = [name for name, data in quest_list.items() if not data.get("new_quests")]
    print(f"  Leaf quests (no follow-ups): {len(leaf_quests)}")
    for lq in sorted(leaf_quests):
        print(f"    - {lq}")
    print()

    if errors:
        print(f"FAILED: {len(errors)} error(s) found.")
        return False
    else:
        print("PASSED: All checks OK.")
        return True


if __name__ == "__main__":
    from quest_list import FIRST_QUESTS, quest_list as ql
    success = validate(ql, FIRST_QUESTS)
    sys.exit(0 if success else 1)
