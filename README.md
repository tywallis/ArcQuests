# ArcQuests

ArcQuests is a small optimizer for planning Arc Raiders quest routes. It validates quest unlock data, builds a greedy route, then runs an ILP solver to search for the shortest route. The best route can be rendered as HTML graphics and captured as PNG screenshots.

## Files

- `quest_list.py` - standard quest data and map enum.
- `bp_quest_list.py` - blueprint-focused quest data.
- `validate.py` - checks quest references, prerequisites, map values, and reachability.
- `greedy_solver.py` - fast baseline route builder.
- `ilp_solver.py` - PuLP/HiGHS optimization model.
- `main.py` - main runner for validation, greedy solve, ILP solve, and results output.
- `generate_graphics.py` - builds `timeline.html` and `checklist.html` from `best_schedule.json`.
- `screenshot.py` - uses Playwright to capture `timeline.png` and `checklist.png`.

## Requirements

This project expects Python 3.12 and the local virtual environment dependencies.

The optimizer uses:

- `pulp`
- `highspy` for the HiGHS solver

The screenshot tool uses:

- `playwright`
- Playwright's Chromium browser

If needed:

```powershell
pip install pulp highspy playwright
python -m playwright install chromium
```

## Run The Standard Quest Optimizer

From the repo folder:

```powershell
$env:PYTHONPATH='.venv\Lib\site-packages'
$env:PYTHONIOENCODING='utf-8'
C:\Python312\python.exe main.py --minutes 60
```

This uses `quest_list.py`, writes the human-readable route to `results.txt`, and saves the machine-readable route to `best_schedule.json`.

`--minutes` controls the solver time limit. The default is 30 minutes.

## Run The Blueprint Optimizer

Only use this when you want the route focused on quests that award blueprints:

```powershell
$env:PYTHONPATH='.venv\Lib\site-packages'
$env:PYTHONIOENCODING='utf-8'
C:\Python312\python.exe main.py --bp --minutes 60
```

This writes `results_bp_quest_list.txt` and `best_schedule_bp_quest_list.json`.

## Optimization Tie-Breakers

The ILP solver prioritizes routes in this order:

1. Fewest total games.
2. Fewest games that require completing more than 3 quests (since time in game is a limited resource).
3. Earlier quest completion when the first two criteria are tied.

## Generate Graphics

After `best_schedule.json` exists:

```powershell
C:\Python312\python.exe generate_graphics.py
```

This regenerates:

- `timeline.html`
- `checklist.html`

Current map colors are hardcoded in `generate_graphics.py`:

- Dam Battlegrounds: green
- Buried City: orange
- Spaceport: red
- Stella Montis: purple
- Blue Gate: blue
- Riven Tides: gray

## Take Screenshots

Start a local static server from the repo folder:

```powershell
C:\Python312\python.exe -m http.server 8080
```

In another PowerShell window, capture the screenshots:

```powershell
$env:PYTHONPATH='.venv\Lib\site-packages'
C:\Python312\python.exe screenshot.py
```

This saves:

- `timeline.png`
- `checklist.png`

## Typical Workflow

1. Update quest data in `quest_list.py`.
2. Run the optimizer:

   ```powershell
   $env:PYTHONPATH='.venv\Lib\site-packages'
   $env:PYTHONIOENCODING='utf-8'
   C:\Python312\python.exe main.py --minutes 60
   ```

3. Generate graphics:

   ```powershell
   C:\Python312\python.exe generate_graphics.py
   ```

4. Start the local server:

   ```powershell
   C:\Python312\python.exe -m http.server 8080
   ```

5. Capture screenshots:

   ```powershell
   $env:PYTHONPATH='.venv\Lib\site-packages'
   C:\Python312\python.exe screenshot.py
   ```
