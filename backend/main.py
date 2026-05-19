from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from time import perf_counter
import asyncio
from concurrent.futures import ThreadPoolExecutor
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

SOLVE_TIMEOUT_SECONDS = 20

executor = ThreadPoolExecutor(max_workers=4)

class MapData(BaseModel):
    w: int
    h: int
    grid: List[str]
    initial_battery: Optional[int] = 100
    initial_oxygen: Optional[int] = 100


@app.get("/")
async def root():
    return {"message": "should work!"}


def build_rescue_heuristic(civilian_positions: set, goal: any):
    def h(state, goal_pos):
        pos = state.robot_position
        unsaved = civilian_positions - state.saved_people

        if not unsaved:
            return abs(pos.x - goal_pos.x) + abs(pos.y - goal_pos.y)

        max_cost = 0
        for p in unsaved:
            cost = (abs(pos.x - p.x) + abs(pos.y - p.y)) + \
                   (abs(p.x - goal_pos.x) + abs(p.y - goal_pos.y))
            if cost > max_cost:
                max_cost = cost

        return max_cost

    return h


def _run_solver(data: MapData) -> dict:
    grid, initial_state, target_pos, civilians, civilian_positions = parse_map(
        data.grid,
        initial_battery=data.initial_battery,
        initial_oxygen=data.initial_oxygen,
        larghezza=data.w,
        altezza=data.h
    )

    print(f"map {data.w}x{data.h} | battery={data.initial_battery} oxygen={data.initial_oxygen}")
    print(f"Robot: {initial_state.robot_position} | Goal: {target_pos} | Civili: {civilians}")

    problem = RescueProblem(
        init=initial_state,
        goal=target_pos,
        grid=grid,
        total_civilians=civilians
    )

    solver = AStar(
        heuristic=build_rescue_heuristic(civilian_positions, target_pos),
        w=2
    )

    search_start = perf_counter()
    plan = solver.solve(problem)
    search_time_ms = round((perf_counter() - search_start) * 1000, 3)

    if plan is None:
        return {
            "success": False,
            "status": "error",
            "message": "Nessun percorso trovato. Il robot è bloccato o ha esaurito le risorse.",
            "search_time_ms": search_time_ms,
            "expanded_nodes": solver.expanded,
            "plan_length": 0,
        }

    print(f"✅ Piano trovato ({len(plan)} step) in {search_time_ms}ms")

    current_state = initial_state
    total_cost = 0
    battery_trace: list[int] = []
    oxygen_trace: list[int] = []

    for action in plan:
        successors = problem.getSuccessors(current_state)
        for act_name, next_state, step_cost in successors:
            if act_name == action:
                current_state = next_state
                total_cost += int(step_cost)
                battery_trace.append(int(current_state.battery))
                oxygen_trace.append(int(current_state.oxygen))
                break

    return {
        "success": True,
        "status": "success",
        "plan": plan,
        "message": "ok",
        "battery_start": data.initial_battery,
        "battery_remaining": current_state.battery,
        "total_cost": total_cost,
        "saved_count": len(current_state.saved_people),
        "extinguisher_charges": current_state.extinguisher_charges,
        "battery_trace": battery_trace,
        "oxygen_trace": oxygen_trace,
        "search_time_ms": search_time_ms,
        "expanded_nodes": solver.expanded,
        "plan_length": len(plan),
    }


@app.post("/solve")
async def solve_task(data: MapData):
    try:
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(executor, _run_solver, data),
            timeout=SOLVE_TIMEOUT_SECONDS
        )
        return result

    except asyncio.TimeoutError:
        print(f"⏱️ Timeout dopo {SOLVE_TIMEOUT_SECONDS}s")
        return {
            "success": False,
            "status": "timeout",
            "message": f"Timeout: nessuna soluzione trovata in {SOLVE_TIMEOUT_SECONDS}s. Prova ad aumentare batteria/ossigeno o semplifica la mappa.",
            "search_time_ms": SOLVE_TIMEOUT_SECONDS * 1000,
            "expanded_nodes": 0,
            "plan_length": 0,
        }

    except ValueError as exc:
        return {
            "success": False,
            "status": "error",
            "message": str(exc),
        }