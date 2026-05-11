"""Generate timeline and checklist graphics from best_schedule.json."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCHEDULE_FILE = ROOT / "best_schedule.json"
TIMELINE_FILE = ROOT / "timeline.html"
CHECKLIST_FILE = ROOT / "checklist.html"

MAP_COLORS = {
    "Dam Battlegrounds": "#22c55e",
    "Buried City": "#f59e0b",
    "Spaceport": "#ef4444",
    "Stella Montis": "#a855f7",
    "Blue Gate": "#3b82f6",
    "Riven Tides": "#64748b",
}


def title_case(text: str) -> str:
    return " ".join(word[:1].upper() + word[1:] for word in text.split(" "))


def load_schedule() -> list[tuple[str, list[str]]]:
    with SCHEDULE_FILE.open(encoding="utf-8") as f:
        return [(map_name, quests) for map_name, quests in json.load(f)]


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def render_legend(map_counts: Counter[str]) -> str:
    items = []
    for map_name, count in map_counts.most_common():
        color = MAP_COLORS.get(map_name, "#64748b")
        items.append(
            f'<div class="legend-item"><span class="legend-dot" style="background:{color}"></span>'
            f"{esc(map_name)} <b>{count}</b></div>"
        )
    return "\n".join(items)


def render_checklist_legend(map_counts: Counter[str]) -> str:
    items = []
    for map_name, count in map_counts.most_common():
        color = MAP_COLORS.get(map_name, "#64748b")
        games_label = "game" if count == 1 else "games"
        items.append(
            f'<div class="legend-item"><span class="legend-dot" style="background:{color}"></span>'
            f"{esc(map_name)} ({count} {games_label})</div>"
        )
    return "\n".join(items)


def render_timeline(schedule: list[tuple[str, list[str]]]) -> str:
    total_games = len(schedule)
    total_quests = sum(len(quests) for _, quests in schedule)
    avg = total_quests / total_games if total_games else 0
    map_counts = Counter(map_name for map_name, _ in schedule)

    rows = []
    for index, (map_name, quests) in enumerate(schedule, 1):
        color = MAP_COLORS.get(map_name, "#64748b")
        quest_items = "\n".join(f"<li>{esc(title_case(q))}</li>" for q in quests)
        rows.append(
            f"""
    <section class="game" style="--map-color:{color}">
      <div class="marker">{index}</div>
      <div class="card">
        <div class="card-head">
          <span class="game-label">Game {index}</span>
          <span class="map-name">{esc(map_name)}</span>
        </div>
        <ul class="quest-list">
          {quest_items}
        </ul>
      </div>
    </section>"""
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Arc Raiders - {total_games} Game Optimal Quest Route</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 42px 20px 56px;
    background: #0a0e17;
    color: #e5edf8;
    font-family: Inter, Arial, sans-serif;
  }}
  .wrap {{ max-width: 980px; margin: 0 auto; }}
  header {{ text-align: center; margin-bottom: 34px; }}
  h1 {{ margin: 0 0 8px; font-size: 40px; line-height: 1.05; font-weight: 900; }}
  .subtitle {{ color: #91a0b8; font-size: 15px; }}
  .stats {{ display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 24px; }}
  .stat {{ min-width: 128px; padding: 14px 18px; border: 1px solid #1f2a3d; background: #101827; border-radius: 8px; }}
  .num {{ display: block; font-size: 28px; font-weight: 900; color: #fff; }}
  .label {{ display: block; margin-top: 2px; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #91a0b8; }}
  .legend {{ display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; margin: 0 0 36px; }}
  .legend-item {{ display: inline-flex; align-items: center; gap: 7px; font-size: 13px; color: #c7d2e3; }}
  .legend-dot {{ width: 10px; height: 10px; border-radius: 999px; display: inline-block; }}
  .timeline {{ position: relative; max-width: 860px; margin: 0 auto; }}
  .timeline::before {{ content: ""; position: absolute; left: 24px; top: 0; bottom: 0; width: 2px; background: #22304a; }}
  .game {{ position: relative; display: grid; grid-template-columns: 64px 1fr; gap: 16px; margin-bottom: 14px; }}
  .marker {{ z-index: 1; width: 50px; height: 50px; border: 3px solid var(--map-color); background: #0a0e17; color: #fff; border-radius: 999px; display: grid; place-items: center; font-weight: 900; }}
  .card {{ border-left: 5px solid var(--map-color); background: #111a2b; border: 1px solid #22304a; border-left-width: 5px; border-radius: 8px; padding: 14px 16px 12px; }}
  .card-head {{ display: flex; justify-content: space-between; gap: 14px; align-items: baseline; margin-bottom: 8px; }}
  .game-label {{ color: #91a0b8; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .8px; }}
  .map-name {{ color: var(--map-color); font-size: 16px; font-weight: 900; }}
  .quest-list {{ margin: 0; padding-left: 18px; columns: 2; column-gap: 28px; }}
  li {{ break-inside: avoid; margin: 4px 0; color: #e5edf8; font-size: 14px; line-height: 1.3; }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Arc Raiders Quest Route</h1>
    <div class="subtitle">Optimized standard quest path</div>
    <div class="stats">
      <div class="stat"><span class="num">{total_games}</span><span class="label">Games</span></div>
      <div class="stat"><span class="num">{total_quests}</span><span class="label">Quests</span></div>
      <div class="stat"><span class="num">{avg:.2f}</span><span class="label">Avg Quests/Game</span></div>
    </div>
  </header>
  <div class="legend">
    {render_legend(map_counts)}
  </div>
  <main class="timeline">
    {"".join(rows)}
  </main>
</div>
</body>
</html>
"""


def render_checklist(schedule: list[tuple[str, list[str]]]) -> str:
    total_games = len(schedule)
    total_quests = sum(len(quests) for _, quests in schedule)
    map_counts = Counter(map_name for map_name, _ in schedule)
    map_total = sum(map_counts.values())

    cards = []
    for index, (map_name, quests) in enumerate(schedule, 1):
        color = MAP_COLORS.get(map_name, "#64748b")
        quest_rows = "\n".join(
            f'<div class="quest-row"><span class="checkbox"></span><span>{esc(title_case(q))}</span></div>'
            for q in quests
        )
        cards.append(
            f"""
    <section class="game-card" style="--map-color:{color}">
      <div class="game-card-header"><span class="game-num">Game {index}</span><span class="map-pill">{esc(map_name.upper())}</span></div>
      {quest_rows}
    </section>"""
        )

    distribution_segments = []
    distribution_labels = []
    for map_name, count in map_counts.most_common():
        color = MAP_COLORS.get(map_name, "#64748b")
        width = (count / map_total * 100) if map_total else 0
        short_name = {
            "Dam Battlegrounds": "Dam",
            "Buried City": "Buried",
            "Spaceport": "Space",
            "Stella Montis": "Stella",
            "Blue Gate": "Blue",
            "Riven Tides": "Riven",
        }.get(map_name, map_name)
        distribution_segments.append(
            f'<div class="dist-segment" style="width:{width:.4f}%; background:{color}"></div>'
        )
        distribution_labels.append(
            f'<div class="dist-label" style="width:{width:.4f}%">{esc(short_name)} {count}</div>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Arc Raiders - Optimal Quest Route</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; padding: 24px; background: #fff; color: #101426; font-family: Inter, Arial, sans-serif; font-size: 11px; }}
  header {{ position: relative; text-align: center; padding-bottom: 12px; margin-bottom: 18px; border-bottom: 3px solid #171827; }}
  h1 {{ margin: 0 0 4px; font-size: 24px; font-weight: 900; letter-spacing: -.2px; }}
  .sub {{ color: #555; font-weight: 600; }}
  .legend {{ display: flex; justify-content: center; gap: 16px; flex-wrap: wrap; margin-bottom: 16px; }}
  .legend-item {{ display: inline-flex; align-items: center; gap: 5px; font-weight: 800; }}
  .legend-dot {{ width: 9px; height: 9px; border-radius: 999px; display: inline-block; }}
  .grid {{ columns: 3; column-gap: 8px; }}
  .game-card {{ border: 1px solid #d4d8e2; border-left: 5px solid var(--map-color); border-radius: 6px; padding: 8px 9px; break-inside: avoid; margin: 0 0 8px; }}
  .game-card-header {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-bottom: 6px; }}
  .game-num {{ color: var(--map-color); font-size: 13px; font-weight: 900; }}
  .map-pill {{ flex: 0 0 auto; color: #fff; background: var(--map-color); border-radius: 999px; padding: 2px 9px 3px; font-size: 8px; font-weight: 900; letter-spacing: .35px; line-height: 1; }}
  .quest-row {{ display: grid; grid-template-columns: 12px 1fr; gap: 5px; align-items: start; margin: 3px 0; line-height: 1.2; }}
  .checkbox {{ width: 10px; height: 10px; border: 1px solid #9ca3af; border-radius: 3px; display: inline-block; margin-top: 1px; }}
  footer {{ margin-top: 26px; padding-top: 12px; border-top: 3px solid #171827; text-align: center; }}
  .dist-title {{ font-weight: 900; font-size: 13px; margin-bottom: 8px; }}
  .dist-bar {{ display: flex; height: 15px; overflow: hidden; border-radius: 999px; }}
  .dist-labels {{ display: flex; color: #8a8f9c; font-size: 9px; margin-top: 4px; }}
  .dist-label {{ text-align: center; white-space: nowrap; }}
  .credit {{ margin-top: 14px; color: #a3a8b3; font-size: 9px; }}
  @media print {{ body {{ padding: 10px; }} }}
</style>
</head>
<body>
  <header>
    <h1>Arc Raiders - Optimal Quest Route</h1>
    <div class="sub">{total_games} Games - {total_quests} Quests - Optimal Route</div>
  </header>
  <div class="legend">
    {render_checklist_legend(map_counts)}
  </div>
  <main class="grid">
    {"".join(cards)}
  </main>
  <footer>
    <div class="dist-title">Map Distribution</div>
    <div class="dist-bar">{"".join(distribution_segments)}</div>
    <div class="dist-labels">{"".join(distribution_labels)}</div>
    <div class="credit">Arc Raiders Quest Optimizer - {total_quests} quests in {total_games} games</div>
  </footer>
</body>
</html>
"""


def main() -> None:
    schedule = load_schedule()
    TIMELINE_FILE.write_text(render_timeline(schedule), encoding="utf-8")
    CHECKLIST_FILE.write_text(render_checklist(schedule), encoding="utf-8")
    total_quests = sum(len(quests) for _, quests in schedule)
    print(f"Generated {TIMELINE_FILE.name} and {CHECKLIST_FILE.name}")
    print(f"Route: {len(schedule)} games, {total_quests} quests")


if __name__ == "__main__":
    main()
