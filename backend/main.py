from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from time import perf_counter
from .logic.parser import parse_map
from .logic.planner import RescueProblem
from .logic.astar_solver import AStar

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app = FastAPI(title="Through The Fire API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MapData(BaseModel):
    w: int
    h: int
    grid: List[str]


@app.get("/")
async def root():
    return {"message": "should work!"}


def manhattan_heuristic(state, goal_pos):
    return abs(state.robot_position.x - goal_pos.x) + abs(state.robot_position.y - goal_pos.y)

def build_rescue_heuristic(civilian_positions: set, goal: Position):
    def h(state, goal_pos):
        pos = state.robot_position
        unsaved = [p for p in civilian_positions if p not in state.saved_people]

        if unsaved:
            dist_to_nearest = min(
                abs(pos.x - p.x) + abs(pos.y - p.y) for p in unsaved
            )
            nearest = min(unsaved, key=lambda p: abs(pos.x - p.x) + abs(pos.y - p.y))
            dist_nearest_to_goal = abs(nearest.x - goal_pos.x) + abs(nearest.y - goal_pos.y)
            return dist_to_nearest + dist_nearest_to_goal
        else:
            return abs(pos.x - goal_pos.x) + abs(pos.y - goal_pos.y)

    return h


def solve_map_payload(data: MapData, verbose: bool = True):
    if verbose:
        print(f"map {data.w}x{data.h}")

    grid, initial_state, target_pos, civilians, civilian_positions = parse_map(
        data.grid, initial_battery=100, larghezza=data.w, altezza=data.h
    )

    if verbose:
        print(f"Posizione Iniziale Robot: {initial_state.robot_position}")
        print(f"Target Civile in: {target_pos}")
        print(f"Civili Totali: {civilians}")

    problem = RescueProblem(init=initial_state, goal=target_pos, grid=grid, total_civilians=civilians)

    solver = AStar(heuristic=build_rescue_heuristic(civilian_positions, target_pos), w=1.5)

    search_start = perf_counter()
    plan = solver.solve(problem)
    search_time_ms = round((perf_counter() - search_start) * 1000, 3)

    if plan is None:
        return {
            "success": False,
            "status": "error",
            "message": "Nessun percorso trovato. Il robot è bloccato o ha finito la batteria.",
            "search_time_ms": search_time_ms,
            "expanded_nodes": solver.expanded,
            "plan_length": 0,
        }

    if verbose:
        print(f"✅ Piano Ottimale Trovato ({len(plan)} step): {plan}")
    else:
        print(f"X nessun piano trovato in {search_time_ms} ms")

    # Ricostruisco lo stato passo-passo per ottenere battery_trace
    current_state = initial_state
    total_cost = 0
    battery_trace: list[int] = []
    oxygen_trace: list[int] = []

    for action in plan:
        successors = problem.getSuccessors(current_state)
        found = False

        # Trova il successore corrispondente a questa azione
        for act_name, next_state, step_cost in successors:
            if act_name == action:
                current_state = next_state
                total_cost += int(step_cost)
                # Registra la batteria dopo aver eseguito l'azione
                batt_val = getattr(current_state, "battery", None)
                battery_trace.append(int(current_state.battery))
                oxygen_trace.append(int(current_state.oxygen))
                found = True
                break

        if not found and verbose:
            print(f"Warning: action '{action}' not found in successors")
            break

    battery_remaining = getattr(current_state, "battery", None)
    saved_count = len(getattr(current_state, "saved_people", ()))
    extinguisher_charges = getattr(current_state, "extinguisher_charges", None)

    return {
        "success": True,
        "status": "success",
        "plan": plan,
        "message": "ok",
        "battery_start": initial_state.battery,
        "battery_remaining": battery_remaining,
        "total_cost": total_cost,
        "saved_count": saved_count,
        "extinguisher_charges": extinguisher_charges,
        "battery_trace": battery_trace,
        "oxygen_trace": oxygen_trace,
        "search_time_ms": search_time_ms,
        "expanded_nodes": solver.expanded,
        "plan_length": len(plan),
    }


@app.post("/solve")
async def solve_task(data: MapData):
    try:
        return solve_map_payload(data, verbose=True)
    except ValueError as exc:
        return {
            "success": False,
            "status": "error",
            "message": str(exc),
        }