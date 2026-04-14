from dataclasses import dataclass
from enum import Enum

class Type(Enum):
    WALL = 0
    BLOCK = 1
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
    pass

