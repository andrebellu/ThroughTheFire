from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .logic import parser

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


@app.post("/solve")
async def solve_task(data: MapData):
    raw_map = parser.parse_map(data.grid)
    print(f"map {data.w}x{data.h}")

    return {
        "success": True,
        "status": "success",
        "plan": ["giù", "destra", "sinistra"],
        "message": "ok",
    }