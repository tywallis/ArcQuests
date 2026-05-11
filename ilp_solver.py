"""
ILP solver: find the provably optimal game sequence using PuLP + CBC.

Variables:
    y[t]     - binary: 1 if game t is played (at least one quest completed)
    x[m,t]   - binary: 1 if map m is chosen at game t
    c[q,t]   - binary: 1 if quest q is completed at or before game t
    z[t]     - binary: 1 if game t completes more than 3 quests

Objective: minimize sum of y[t]

Constraints:
    1. One map per game: sum_m x[m,t] = y[t]
    2. Quest needs its map: c[q,t] - c[q,t-1] <= sum_{m in maps(q)} x[m,t]
    3. OR-unlock: a quest q can only be completed at time t if it's "available".
       - For FIRST_QUESTS: always available (no constraint).
       - For quests WITH prerequisites: available if ALL prerequisites done by t-1.
       - For quests WITHOUT prerequisites (but not in FIRST_QUESTS): available if
         ANY parent (quest whose new_quests contains q) is done by t-1.
    4. All quests done by T_max: c[q, T_max] = 1
    5. Monotonicity: c[q,t] >= c[q,t-1]
    6. Symmetry breaking: y[t] >= y[t+1]
"""

import os

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value, HiGHS

from quest_list import Maps


def build_parent_map(quest_list: dict) -> dict[str, list[str]]:
    """Build reverse mapping: for each quest, which quests list it in new_quests."""
    parents: dict[str, list[str]] = {q: [] for q in quest_list}
    for quest_name, data in quest_list.items():
        for nq in data.get("new_quests", []):
            if nq in parents:
                parents[nq].append(quest_name)
    return parents


def _read_sol_file(prob: LpProblem, sol_path: str) -> None:
    """Read a CBC .sol file and set variable values on the problem."""
    var_dict = {v.name: v for v in prob.variables()}
    with open(sol_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                # Format: <index> <varname> <value> ...
                name = parts[1]
                try:
                    val = float(parts[2])
                except (ValueError, IndexError):
                    continue
                if name in var_dict:
                    var_dict[name].varValue = val


def ilp_solve(
    quest_list: dict,
    first_quests: list[str],
    t_max: int,
    warm_start: list[tuple[Maps, list[str]]] | None = None,
    time_limit: int = 1800,
) -> list[tuple[Maps, list[str]]] | None:
    """
    Solve the quest scheduling problem optimally using ILP.

    Args:
        t_max: upper bound on number of games (e.g. from greedy solver).
        warm_start: an existing feasible schedule (e.g. from greedy) to seed CBC.
        time_limit: maximum solver runtime in seconds.

    Returns:
        Best schedule found as list of (map, [quests]) tuples, or None if infeasible.
    """
    quests = list(quest_list.keys())
    maps_list = list(Maps)
    time_steps = list(range(1, t_max + 1))
    parents = build_parent_map(quest_list)
    first_quests_set = set(first_quests)

    prob = LpProblem("ArcQuests_Optimal", LpMinimize)

    # --- Variables ---
    y = {t: LpVariable(f"y_{t}", cat="Binary") for t in time_steps}
    z = {t: LpVariable(f"z_more_than_3_quests_{t}", cat="Binary") for t in time_steps}
    x = {
        (m, t): LpVariable(f"x_{m.name}_{t}", cat="Binary")
        for m in maps_list
        for t in time_steps
    }
    c = {
        (q, t): LpVariable(f"c_{q}_{t}", cat="Binary")
        for q in quests
        for t in time_steps
    }
    # c[q, 0] = 0 for all q (nothing completed before game 1)
    c0 = {q: 0 for q in quests}

    completed_at = {
        (q, t): c[(q, t)] - (c[(q, t - 1)] if t > 1 else c0[q])
        for q in quests
        for t in time_steps
    }

    # --- Objective: minimize games, then busy games, then front-load quests ---
    # Primary: minimize number of games played
    # Secondary: minimize games that complete more than 3 quests
    # Tertiary: minimize sum of completion times (pushes quests earlier)
    # Weights are small enough that tie-breakers never add an extra game.
    busy_game_weight = 1.0 / (t_max + 1)
    frontload_weight = 1.0 / ((t_max + 1) * (len(quests) * t_max + 1))
    prob += (
        lpSum(y[t] for t in time_steps)
        + busy_game_weight * lpSum(z[t] for t in time_steps)
        + frontload_weight * lpSum(t * completed_at[(q, t)] for q in quests for t in time_steps),
        "MinimizeGames_LimitBusyGames_FrontLoaded",
    )

    # --- Constraint 1: one map per game ---
    for t in time_steps:
        prob += (
            lpSum(x[m, t] for m in maps_list) == y[t],
            f"OneMapPerGame_{t}",
        )

    # --- Constraint 2: quest needs its map played to be completed ---
    for q in quests:
        quest_maps = quest_list[q]["maps"]
        for t in time_steps:
            c_prev = c[(q, t - 1)] if t > 1 else c0[q]
            prob += (
                c[(q, t)] - c_prev <= lpSum(x[m, t] for m in quest_maps),
                f"QuestNeedsMap_{q}_{t}",
            )

    # --- Constraint 3: availability ---
    for q in quests:
        prereqs = quest_list[q].get("prerequisites", [])

        if q in first_quests_set and not prereqs:
            # FIRST_QUESTS with no prerequisites: always available, no constraint
            pass

        elif prereqs:
            # AND-gate: ALL prerequisites must be completed before this quest
            for t in time_steps:
                c_prev_q = c[(q, t - 1)] if t > 1 else c0[q]
                for p in prereqs:
                    c_prev_p = c[(p, t - 1)] if t > 1 else c0[p]
                    prob += (
                        c[(q, t)] - c_prev_q <= c_prev_p,
                        f"Prereq_{q}_{p}_{t}",
                    )

        else:
            # OR-unlock: at least one parent must be completed before this quest
            parent_list = parents[q]
            if parent_list:
                for t in time_steps:
                    c_prev_q = c[(q, t - 1)] if t > 1 else c0[q]
                    prob += (
                        c[(q, t)] - c_prev_q <= lpSum(
                            (c[(p, t - 1)] if t > 1 else c0[p]) for p in parent_list
                        ),
                        f"ORUnlock_{q}_{t}",
                    )

    # --- Constraint 4: all quests completed by T_max ---
    for q in quests:
        prob += c[(q, t_max)] == 1, f"AllDone_{q}"

    # --- Constraint 5: monotonicity ---
    for q in quests:
        for t in time_steps:
            c_prev = c[(q, t - 1)] if t > 1 else c0[q]
            prob += c[(q, t)] >= c_prev, f"Mono_{q}_{t}"

    # --- Constraint 6: symmetry breaking (games are front-loaded) ---
    for t in time_steps[:-1]:
        prob += y[t] >= y[t + 1], f"SymBreak_{t}"

    # --- Constraint 7: mark games that complete more than 3 quests ---
    for t in time_steps:
        prob += (
            lpSum(completed_at[(q, t)] for q in quests) - 3 <= len(quests) * z[t],
            f"MoreThan3Quests_{t}",
        )

    # --- Warm-start from greedy solution ---
    if warm_start is not None:
        print("Setting warm-start from greedy solution...")
        # Build the completion timeline from the greedy schedule
        completed_by: dict[str, int] = {}  # quest -> time step when completed
        for step_idx, (ws_map, ws_quests) in enumerate(warm_start, 1):
            for q_name in ws_quests:
                completed_by[q_name] = step_idx

        # Set initial values for all variables
        num_greedy_games = len(warm_start)
        for t in time_steps:
            # y[t]: game is played if t <= num_greedy_games
            y[t].setInitialValue(1 if t <= num_greedy_games else 0)

            # x[m,t]: which map was chosen at time t
            if t <= num_greedy_games:
                ws_map_t = warm_start[t - 1][0]
                for m in maps_list:
                    x[(m, t)].setInitialValue(1 if m == ws_map_t else 0)
            else:
                for m in maps_list:
                    x[(m, t)].setInitialValue(0)

            # c[q,t]: quest completed at or before time t
            for q in quests:
                done_at = completed_by.get(q, t_max + 1)
                c[(q, t)].setInitialValue(1 if t >= done_at else 0)

    # --- Solve ---
    print(f"ILP: {len(quests)} quests, {len(maps_list)} maps, {t_max} max games")
    print(f"ILP: {len(prob.variables())} variables, {len(prob.constraints)} constraints")
    print("Solving...")

    solver = HiGHS(msg=1, timeLimit=time_limit, warmStart=True if warm_start else False)
    try:
        prob.solve(solver)
    except KeyboardInterrupt:
        print("\n*** Solver interrupted by user ***")

    status = LpStatus.get(prob.status, "Undefined")
    print(f"ILP status: {status}")

    # Check if we have any solution to extract
    obj_val = value(prob.objective)

    if obj_val is None:
        print("No feasible solution found.")
        return None

    if status == "Optimal":
        print(f"Proven optimal: {int(obj_val)} games")
    else:
        print(f"Best feasible solution found: {int(obj_val)} games (status: {status})")

    # --- Extract schedule ---
    schedule: list[tuple[Maps, list[str]]] = []
    for t in time_steps:
        if value(y[t]) is None or value(y[t]) < 0.5:
            continue

        # Find which map was chosen
        chosen_map = None
        for m in maps_list:
            if value(x[m, t]) is not None and value(x[m, t]) > 0.5:
                chosen_map = m
                break

        if chosen_map is None:
            continue

        # Find which quests were completed at this time step
        completed_this_step = []
        for q in quests:
            c_prev_val = value(c[(q, t - 1)]) if t > 1 else 0
            c_cur_val = value(c[(q, t)])
            if c_prev_val is not None and c_cur_val is not None:
                if c_cur_val > 0.5 and (c_prev_val < 0.5):
                    completed_this_step.append(q)

        if completed_this_step:
            schedule.append((chosen_map, sorted(completed_this_step)))

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
    for i, (map_choice, quests_done) in enumerate(schedule, 1):
        lines.append(f"Game {i}: {map_choice.value}")
        for q in quests_done:
            lines.append(f"    \u2022 {_title_case(q)}")
    lines.append("-" * 60)
    return "\n".join(lines)


def print_schedule(schedule: list[tuple[Maps, list[str]]]) -> None:
    """Pretty-print a game schedule."""
    print(format_schedule(schedule))


if __name__ == "__main__":
    from greedy_solver import greedy_solve
    from quest_list import FIRST_QUESTS, quest_list as ql

    # Use greedy result as upper bound
    greedy_schedule = greedy_solve(ql, FIRST_QUESTS)
    t_max = len(greedy_schedule)
    print(f"\nGreedy found {t_max} games. Using as T_max for ILP.\n")

    schedule = ilp_solve(ql, FIRST_QUESTS, t_max)
    if schedule:
        print("\n=== ILP OPTIMAL RESULT ===")
        print_schedule(schedule)
