from models import Position, State, CellType
from typing import List, Set, Tuple

DIRECTIONS = {
    "UP": Position(0, -1),
    "DOWN": Position(0, 1),
    "LEFT": Position(-1, 0),
    "RIGHT": Position(1, 0),
}

def get_successors(current_state: State, grid: List[List[CellType]]):
    pass