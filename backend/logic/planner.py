from models import Position, State, CellType
from typing import List, Set, Tuple

DIRECTIONS = {
    "UP": Position(0, -1),
    "DOWN": Position(0, 1),
    "LEFT": Position(-1, 0),
    "RIGHT": Position(1, 0),
}


def get_successors(current_state: State, grid: List[List[CellType]]) -> List[Tuple[str, State, int]] | None:
    successors = []

    if not grid:
        return successors

    max_x = len(grid[0])
    max_y = len(grid)

    # movement
    for action_name, direction in DIRECTIONS.items():
        print(action_name)
        print(direction)
        print(current_state)
        new_position = current_state.robot_position + direction

        if 0 <= new_position.x < max_x and 0 <= new_position.y < max_y:
            if grid[new_position.x][new_position.y] != CellType.WALL:

                if current_state.battery > 0:
                    new_state = State(
                        robot_position=new_position,
                        battery=current_state.battery,
                        saved_people=current_state.saved_people,
                        extinguished_fires=current_state.extinguished_fires,
                        g=current_state.g,
                        h=0  # TODO: heuristic function
                    )

                    cost = 0
                    successors.append((action_name, new_state, cost))

    # TODO: implement civil rescue logic
    return None
