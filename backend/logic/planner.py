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

        def isGoal(self, state) -> bool:
            return self.goal in state.saved_people

DIRECTIONS = {
    "UP": Position(0, -1),
    "DOWN": Position(0, 1),
    "LEFT": Position(-1, 0),
    "RIGHT": Position(1, 0),
}

def get_heuristic(current_pos: Position, target_pos: Position) -> int:
    return abs(current_pos.x - target_pos.x) + abs(current_pos.y - target_pos.y)

def get_successors(current_state: State, grid: List[List[CellType]], target_pos: Position) -> List[Tuple[str, State, int]]:
    successors = []

    if not grid:
        return successors

    max_x = len(grid[0])
    max_y = len(grid)

    # movement
    for action_name, direction in DIRECTIONS.items():
        new_position = current_state.robot_position + direction

        if 0 <= new_position.x < max_x and 0 <= new_position.y < max_y:
            target_cell = grid[new_position.y][new_position.x]

            if target_cell != CellType.WALL:

                battery_cost = 1
                new_charges = current_state.extinguisher_charges
                new_extinguished = set(current_state.extinguished_fires)

                if target_cell == CellType.FIRE and new_position not in current_state.extinguished_fires:
                    if current_state.extinguisher_charges > 0:
                        # Usiamo l'estintore senza danni
                        new_charges -= 1
                        new_extinguished.add(new_position)
                    else:

                        battery_cost = 10

                if current_state.battery >= battery_cost:

                    new_state = State(
                        robot_position=new_position,
                        battery=current_state.battery - battery_cost,
                        saved_people=current_state.saved_people,
                        extinguished_fires=frozenset(new_extinguished),
                        collected_extinguishers=current_state.collected_extinguishers,
                        extinguisher_charges=new_charges,
                        g=current_state.g + 1,
                        h=get_heuristic(new_position, target_pos)
                    )

                    cost = 1
                    successors.append((action_name, new_state, cost))

    robot_pos = current_state.robot_position

    if grid[robot_pos.y][robot_pos.x] == CellType.PERSON and robot_pos not in current_state.saved_people:
        new_saved_people = set(current_state.saved_people)
        new_saved_people.add(robot_pos)

        new_state = State(
            robot_position=current_state.robot_position,
            battery=current_state.battery - 5,
            saved_people=frozenset(new_saved_people),
            extinguished_fires=current_state.extinguished_fires,
            g =current_state.g + 1,
            h = get_heuristic(current_state.robot_position, target_pos)
        )

        cost = 1
        successors.append(("RESCUE", new_state, cost))

    if grid[robot_pos.y][robot_pos.x] == CellType.EXTINGUISHER and robot_pos not in current_state.collected_extinguishers:

        new_collected = set(current_state.collected_extinguishers)
        new_collected.add(robot_pos)

        new_state = State(
            robot_position=current_state.robot_position,
            battery=current_state.battery - 1,
            saved_people=current_state.saved_people,
            extinguished_fires=current_state.extinguished_fires,
            collected_extinguishers=frozenset(new_collected),
            extinguisher_charges=current_state.extinguisher_charges + 1,
            g=current_state.g + 1,
            h=get_heuristic(current_state.robot_position, target_pos)
        )

        cost = 1
        successors.append(("PICK_EXTINGUISHER", new_state, cost))

    return successors


