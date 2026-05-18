from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet

class CellType(Enum):
    WALL = 0
    EMPTY = 1
    FIRE = 2
    PERSON = 3
    EXTINGUISHER = 4
    GOAL = 9

@dataclass(frozen=True, order=True)
class Position:
    x: int
    y: int

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

@dataclass(frozen=True)
class State:
    robot_position: Position
    battery: int
    saved_people: FrozenSet[Position]
    extinguished_fires: FrozenSet[Position]
    collected_extinguishers: FrozenSet[Position]
    extinguisher_charges: int
    oxygen: int = 100
    oxygen_active: bool = False
    g: int = 0
    h: int = 0

    @property
    def f(self) -> int:
        return self.g + self.h

    def __lt__(self, other):
        if self.f == other.f:
            return self.g > other.g
        return self.f < other.f