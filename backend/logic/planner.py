from .models import Position, State, CellType
from typing import List, Set, Tuple
from .search_problem import SearchProblem
from dataclasses import replace


class RescueProblem(SearchProblem):
    def __init__(self, init: State, goal: Position, grid: list[list[CellType]], cost: dict = None):
        if cost is None:
            cost = {"move": 1, "rescue": 1}

        super().__init__(init, goal, cost)
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0

    def isGoal(self, state: State) -> bool:
        return self.goal in state.saved_people

    def getSuccessors(self, state: State) -> list:
        successors = []

        if state.battery <= 0:
            return successors

        x = state.robot_position.x
        y = state.robot_position.y


        if state.robot_position == self.goal and self.goal not in state.saved_people:
            new_state = replace(
                state,
                saved_people=state.saved_people | frozenset([self.goal]),
                battery=state.battery - self.cost.get("rescue", 1)
            )
            successors.append(("RESCUE", new_state, self.cost.get("rescue", 1)))


        moves = {
            "su": Position(x, y - 1),
            "giù": Position(x, y + 1),
            "sinistra": Position(x - 1, y),
            "destra": Position(x + 1, y)
        }

        for action_name, new_pos in moves.items():
            if 0 <= new_pos.y < self.height and 0 <= new_pos.x < self.width:
                if self.grid[new_pos.y][new_pos.x] != CellType.WALL:
                    new_state = replace(
                        state,
                        robot_position=new_pos,
                        battery=state.battery - self.cost.get("move", 1)
                    )
                    successors.append((action_name, new_state, self.cost.get("move", 1)))

        return successors


