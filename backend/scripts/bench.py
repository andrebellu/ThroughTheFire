import random
import time
import csv
import os
import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from logic.models import CellType, Position, State
from logic.planner import RescueProblem
from logic.astar_solver import AStar

SEED = 42
TRIALS_PER_CFG = 5
INITIAL_BATTERY = 300
INITIAL_OXYGEN = 300
W = 2
TIMEOUT_S = 30

SIZES = [(8, 8), (10, 10), (12, 10), (14, 12), (16, 12), (18, 14), (20, 15)]
CIVILIAN_COUNTS = [1, 2, 3, 4]
FIRE_DENSITIES = [0.05, 0.10, 0.15]

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

PREDEFINED_LEVELS = [
    {
        "nome": "Through the Smoke",
        "difficolta": "Easy",
        "larghezza": 10,
        "altezza": 8,
        "schema": (
            "##########"
            "#R.......#"
            "####.###.#"
            "#..P...#.#"
            "#.####.F.#"
            "#C.....E.#"
            "#......F.#"
            "########MA"
        )
    },
    {
        "nome": "Through the Fire",
        "difficolta": "Medium",
        "larghezza": 14,
        "altezza": 10,
        "schema": (
            "##############"
            "#R.......E..P#"
            "###.####.###M#"
            "#C..#F.....MC#"
            "#F###.####.###"
            "#.#........#.#"
            "#.#.######F#.#"
            "#..........E.#"
            "#F.#######.F.#"
            "###########.A#"
        )
    },
    {
        "nome": "Through Hell",
        "difficolta": "Hard",
        "larghezza": 16,
        "altezza": 12,
        "schema": (
            "################"
            "#R...F.....C...#"
            "#.####.###.###.#"
            "#.#C...F.#M#E..#"
            "#.######.#.#.###"
            "#P.....E.#...#.#"
            "######M#####.#.#"
            "#F...#.......#.#"
            "#.##.#####.###.#"
            "#.#C.F.......F.#"
            "#...E.####.C...#"
            "##############A#"
        )
    },
    {
        "nome": "Ultra Hell",
        "difficolta": "Ultra",
        "larghezza": 18,
        "altezza": 14,
        "schema": (
            "##################"
            "#R.F......P..#...#"
            "#.##.#######.#M#.#"
            "#.#C.......F.#.#.#"
            "#.#.##########.#.#"
            "#.F.MC...#...F...#"
            "#####.##.#.###E#.#"
            "#...#..#F#...#.#.#"
            "#.####.#.###.#MF.#"
            "#.#E...#...C.#.#.#"
            "#...F..###.###...#"
            "#.####C#...F.#.###"
            "#......#E..#.....#"
            "################A#"
        )
    },
    {
        "nome": "Ultra Ultra Hell",
        "difficolta": "Nightmare",
        "larghezza": 20,
        "altezza": 15,
        "schema": (
            "####################"
            "#R..#....MCM...#P..#"
            "#F..#.####M###M#F#.#"
            "#...#.#E.......#.#.#"
            "###.#.#.######.#.#.#"
            "#C..F...#C...F...#.#"
            "#.#######M####M###M#"
            "#.......#.#E.......#"
            "#######.#.#.######.#"
            "#...F...#...#C...F.#"
            "#.#######M###.####.#"
            "#.#E......#......#.#"
            "#...F...###.C..F...#"
            "#..##...E.#...##...#"
            "##################A#"
        )
    },
]

CHAR_MAP = {
    '#': CellType.WALL,
    '.': CellType.EMPTY,
    'F': CellType.FIRE,
    'C': CellType.PERSON,
    'A': CellType.GOAL,
    'E': CellType.EXTINGUISHER,
    'R': CellType.EMPTY,
    'M': CellType.RUBBLE,
    'P': CellType.PICKAXE,
}


def parse_schema(schema: str, w: int, h: int, battery: int, oxygen: int):
    grid = []
    robot_pos = None
    civilians = set()
    exit_pos = None
    has_pickaxe_on_map = False

    for y in range(h):
        row = []
        for x in range(w):
            ch = schema[y * w + x]
            pos = Position(x, y)
            if ch == 'R':
                robot_pos = pos
            elif ch == 'C':
                civilians.add(pos)
            elif ch == 'A':
                exit_pos = pos
            elif ch == 'P':
                has_pickaxe_on_map = True
            row.append(CHAR_MAP.get(ch, CellType.EMPTY))
        grid.append(row)

    if robot_pos is None or exit_pos is None:
        return None, None, None, None, None

    state = State(
        robot_position=robot_pos,
        battery=battery,
        saved_people=frozenset(),
        extinguished_fires=frozenset(),
        collected_extinguishers=frozenset(),
        extinguisher_charges=0,
        oxygen=oxygen,
        oxygen_active=False,
        has_pickaxe=False,
        cleared_rubble=frozenset(),
        g=0,
        h=0,
    )
    return grid, state, exit_pos, len(civilians), civilians


def build_heuristic(civilian_positions: set):
    def h(state, goal_pos):
        pos = state.robot_position
        unsaved = civilian_positions - state.saved_people
        if not unsaved:
            return abs(pos.x - goal_pos.x) + abs(pos.y - goal_pos.y)
        return max(
            abs(pos.x - c.x) + abs(pos.y - c.y) +
            abs(c.x - goal_pos.x) + abs(c.y - goal_pos.y)
            for c in unsaved
        )

    return h


def run_once(grid, init_state, goal_pos, n_civilians, civilian_positions):
    problem = RescueProblem(
        init=init_state,
        goal=goal_pos,
        grid=grid,
        total_civilians=n_civilians,
    )
    solver = AStar(
        heuristic=build_heuristic(civilian_positions),
        w=W,
        view=True,
    )
    t0 = time.perf_counter()
    plan = solver.solve(problem)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    return {
        "solved": plan is not None,
        "time_ms": round(elapsed_ms, 2),
        "nodes_expanded": solver.expanded,
        "plan_length": len(plan) if plan else 0,
    }


def random_map(w: int, h: int, n_civilians: int, fire_density: float, rng: random.Random):
    grid_chars = [['.' for _ in range(w)] for _ in range(h)]

    for x in range(w):
        grid_chars[0][x] = '#'
        grid_chars[h - 1][x] = '#'
    for y in range(h):
        grid_chars[y][0] = '#'
        grid_chars[y][w - 1] = '#'

    grid_chars[1][1] = 'R'
    grid_chars[h - 2][w - 2] = 'A'

    free = [
        (x, y)
        for y in range(1, h - 1)
        for x in range(1, w - 1)
        if grid_chars[y][x] == '.'
    ]
    rng.shuffle(free)

    placed = 0
    idx = 0
    while placed < n_civilians and idx < len(free):
        x, y = free[idx];
        idx += 1
        grid_chars[y][x] = 'C'
        placed += 1

    if placed < n_civilians:
        return None

    remaining = [(x, y) for x, y in free[idx:] if grid_chars[y][x] == '.']

    n_fires = max(1, int(len(remaining) * fire_density))
    for x, y in remaining[:n_fires]:
        grid_chars[y][x] = 'F'

    n_ext = max(1, n_fires // 3)
    ext_start = n_fires
    for x, y in remaining[ext_start:ext_start + n_ext]:
        grid_chars[y][x] = 'E'

    debris_start = ext_start + n_ext
    n_debris = max(0, int(len(remaining) * 0.05))
    for x, y in remaining[debris_start:debris_start + n_debris]:
        grid_chars[y][x] = 'M'

    if n_debris > 0:
        pick_start = debris_start + n_debris
        pool = remaining[pick_start:pick_start + 3]
        if pool:
            x, y = pool[0]
            grid_chars[y][x] = 'P'

    schema = ''.join(grid_chars[y][x] for y in range(h) for x in range(w))
    return schema


def benchmark_predefined():
    print("\n=== Livelli predefiniti ===")
    rows = []

    for lvl in PREDEFINED_LEVELS:
        w, h = lvl["larghezza"], lvl["altezza"]
        schema = lvl["schema"].replace('\n', '').replace(' ', '')

        grid, init_state, goal_pos, n_civ, civ_pos = parse_schema(
            schema, w, h, INITIAL_BATTERY, INITIAL_OXYGEN
        )
        if grid is None:
            print(f"  [SKIP] {lvl['nome']} — parsing fallito")
            continue

        result = run_once(grid, init_state, goal_pos, n_civ, civ_pos)

        row = {
            "nome": lvl["nome"],
            "difficolta": lvl["difficolta"],
            "w": w,
            "h": h,
            "map_cells": w * h,
            "civilians": n_civ,
            **result,
        }
        rows.append(row)

        status = "✅" if result["solved"] else "❌"
        print(f"  {status} {lvl['nome']:20s} | "
              f"{w}×{h} | "
              f"civili={n_civ} | "
              f"time={result['time_ms']:8.1f}ms | "
              f"nodes={result['nodes_expanded']:7d} | "
              f"steps={result['plan_length']}")

    return rows


def benchmark_random():
    print("\n=== Mappe casuali ===")
    rng = random.Random(SEED)
    rows = []

    total = len(SIZES) * len(CIVILIAN_COUNTS) * len(FIRE_DENSITIES) * TRIALS_PER_CFG
    done = 0

    for (w, h) in SIZES:
        for n_civ in CIVILIAN_COUNTS:
            for fd in FIRE_DENSITIES:
                times, nodes, solved_count = [], [], 0

                for trial in range(TRIALS_PER_CFG):
                    schema = random_map(w, h, n_civ, fd, rng)
                    if schema is None:
                        done += 1
                        continue

                    grid, init_state, goal_pos, nc, civ_pos = parse_schema(
                        schema, w, h, INITIAL_BATTERY, INITIAL_OXYGEN
                    )
                    if grid is None:
                        done += 1
                        continue

                    result = run_once(grid, init_state, goal_pos, nc, civ_pos)
                    done += 1

                    if result["solved"]:
                        times.append(result["time_ms"])
                        nodes.append(result["nodes_expanded"])
                        solved_count += 1

                    print(f"  [{done:3d}/{total}] {w}×{h} civ={n_civ} fd={fd:.0%} "
                          f"trial={trial + 1} | "
                          f"{'OK' if result['solved'] else 'FAIL':4s} "
                          f"{result['time_ms']:8.1f}ms "
                          f"nodes={result['nodes_expanded']:7d}")

                row = {
                    "w": w,
                    "h": h,
                    "map_cells": w * h,
                    "civilians": n_civ,
                    "fire_density": fd,
                    "trials": TRIALS_PER_CFG,
                    "solved": solved_count,
                    "time_ms_median": round(np.median(times), 2) if times else None,
                    "time_p25": round(np.percentile(times, 25), 2) if times else None,
                    "time_p75": round(np.percentile(times, 75), 2) if times else None,
                    "nodes_median": round(np.median(nodes), 1) if nodes else None,
                    "nodes_p25": round(np.percentile(nodes, 25), 1) if nodes else None,
                    "nodes_p75": round(np.percentile(nodes, 75), 1) if nodes else None,
                }
                rows.append(row)

    return rows


def save_csv(rows, filename):
    if not rows:
        return
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSalvato: {path}")


COLORS = ['#378ADD', '#1D9E75', '#EF9F27', '#D85A30']


def plot_time_vs_civilians(random_rows):
    fig, ax = plt.subplots(figsize=(7, 4))

    for i, (w, h) in enumerate([(10, 10), (14, 12), (16, 12), (20, 15)]):
        subset = [r for r in random_rows if r["w"] == w and r["h"] == h
                  and r["fire_density"] == 0.10 and r["time_ms_median"] is not None]
        if not subset:
            continue
        xs = [r["civilians"] for r in subset]
        ys = [r["time_ms_median"] for r in subset]

        yerr_lower = [r["time_ms_median"] - r["time_p25"] for r in subset]
        yerr_upper = [r["time_p75"] - r["time_ms_median"] for r in subset]

        ax.errorbar(xs, ys, yerr=[yerr_lower, yerr_upper], marker='o', label=f"{w}×{h}",
                    color=COLORS[i % len(COLORS)], capsize=4, linewidth=1.5)

    ax.set_yscale('log')
    ax.set_xlabel("Numero di civili")
    ax.set_ylabel("Tempo Mediano (ms)")
    ax.set_title("Tempo di risoluzione vs. civili (densità fuochi 10%)")
    ax.legend(title="Dimensione mappa")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.0f}"))
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "plot_time_vs_civilians.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Salvato: {path}")


def plot_nodes_vs_civilians(random_rows):
    fig, ax = plt.subplots(figsize=(7, 4))

    for i, (w, h) in enumerate([(10, 10), (14, 12), (16, 12), (20, 15)]):
        subset = [r for r in random_rows if r["w"] == w and r["h"] == h
                  and r["fire_density"] == 0.10 and r["nodes_median"] is not None]
        if not subset:
            continue
        xs = [r["civilians"] for r in subset]
        ys = [r["nodes_median"] for r in subset]

        yerr_lower = [r["nodes_median"] - r["nodes_p25"] for r in subset]
        yerr_upper = [r["nodes_p75"] - r["nodes_median"] for r in subset]

        ax.errorbar(xs, ys, yerr=[yerr_lower, yerr_upper], marker='s', label=f"{w}×{h}",
                    color=COLORS[i % len(COLORS)], capsize=4, linewidth=1.5)

    ax.set_yscale('log')
    ax.set_xlabel("Numero di civili")
    ax.set_ylabel("Nodi espansi (Mediana)")
    ax.set_title("Nodi espansi vs. civili (densità fuochi 10%)")
    ax.legend(title="Dimensione mappa")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "plot_nodes_vs_civilians.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Salvato: {path}")


def plot_time_vs_mapsize(random_rows):
    fig, ax = plt.subplots(figsize=(7, 4))

    for i, nc in enumerate(CIVILIAN_COUNTS):
        subset = [r for r in random_rows if r["civilians"] == nc
                  and r["fire_density"] == 0.10 and r["time_ms_median"] is not None]
        if not subset:
            continue
        subset.sort(key=lambda r: r["map_cells"])
        xs = [r["map_cells"] for r in subset]
        ys = [r["time_ms_median"] for r in subset]

        yerr_lower = [r["time_ms_median"] - r["time_p25"] for r in subset]
        yerr_upper = [r["time_p75"] - r["time_ms_median"] for r in subset]

        ax.errorbar(xs, ys, yerr=[yerr_lower, yerr_upper], marker='o', label=f"{nc} civili",
                    color=COLORS[i % len(COLORS)], capsize=4, linewidth=1.5)

    ax.set_yscale('log')
    ax.set_xlabel("Celle totali (w × h)")
    ax.set_ylabel("Tempo Mediano (ms)")
    ax.set_title("Tempo di risoluzione vs. dimensione mappa (densità fuochi 10%)")
    ax.legend(title="Civili")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "plot_time_vs_mapsize.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Salvato: {path}")


def plot_nodes_vs_mapsize(random_rows):
    fig, ax = plt.subplots(figsize=(7, 4))

    for i, nc in enumerate(CIVILIAN_COUNTS):
        subset = [r for r in random_rows if r["civilians"] == nc
                  and r["fire_density"] == 0.10 and r["nodes_median"] is not None]
        if not subset:
            continue
        subset.sort(key=lambda r: r["map_cells"])
        xs = [r["map_cells"] for r in subset]
        ys = [r["nodes_median"] for r in subset]

        yerr_lower = [r["nodes_median"] - r["nodes_p25"] for r in subset]
        yerr_upper = [r["nodes_p75"] - r["nodes_median"] for r in subset]

        ax.errorbar(xs, ys, yerr=[yerr_lower, yerr_upper], marker='s', label=f"{nc} civili",
                    color=COLORS[i % len(COLORS)], capsize=4, linewidth=1.5)

    ax.set_yscale('log')
    ax.set_xlabel("Celle totali (w × h)")
    ax.set_ylabel("Nodi espansi (Mediana)")
    ax.set_title("Nodi espansi vs. dimensione mappa (densità fuochi 10%)")
    ax.legend(title="Civili")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "plot_nodes_vs_mapsize.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Salvato: {path}")


def plot_predefined_table(pred_rows):
    solved = [r for r in pred_rows if r["solved"]]
    if not solved:
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    names = [r["nome"] for r in solved]
    times = [r["time_ms"] for r in solved]
    nodes = [r["nodes_expanded"] for r in solved]

    ax1.barh(names, times, color=COLORS[0], alpha=0.85)
    ax1.set_xlabel("Tempo (ms)")
    ax1.set_title("Tempo di risoluzione — livelli predefiniti")
    ax1.grid(True, axis='x', alpha=0.3)

    ax2.barh(names, nodes, color=COLORS[1], alpha=0.85)
    ax2.set_xlabel("Nodi espansi")
    ax2.set_title("Nodi espansi — livelli predefiniti")
    ax2.grid(True, axis='x', alpha=0.3)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "plot_predefined.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Salvato: {path}")


if __name__ == "__main__":
    pred_rows = benchmark_predefined()
    random_rows = benchmark_random()

    save_csv(pred_rows, "results_predefined.csv")
    save_csv(random_rows, "results_random.csv")

    plot_predefined_table(pred_rows)
    plot_time_vs_civilians(random_rows)
    plot_nodes_vs_civilians(random_rows)
    plot_time_vs_mapsize(random_rows)
    plot_nodes_vs_mapsize(random_rows)

    print("\nBenchmark completato.")