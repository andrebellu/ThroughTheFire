from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
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
    if goal_pos in state.saved_people:
        return 0
    return abs(state.robot_position.x - goal_pos.x) + abs(state.robot_position.y - goal_pos.y)

@app.post("/solve")
async def solve_task(data: MapData):
    print(f"map {data.w}x{data.h}")

    grid, initial_state, target_pos = parse_map(
        data.grid,
        initial_battery=100,
        larghezza=data.w,
        altezza=data.h
    )

    print(f"Posizione Iniziale Robot: {initial_state.robot_position}")
    print(f"Target Civile in: {target_pos}")

    problem = RescueProblem(init=initial_state, goal=target_pos, grid=grid)

    solver = AStar(heuristic=manhattan_heuristic)

    plan = solver.solve(problem)

    if plan is None:
        return {
            "success": False,
            "status": "error",
            "message": "Nessun percorso trovato. Il robot è bloccato o ha finito la batteria."
        }

    print(f"✅ Piano Ottimale Trovato ({len(plan)} step): {plan}")

    return {
        "success": True,
        "status": "success",
        "plan": plan,
        "message": "ok",
    }