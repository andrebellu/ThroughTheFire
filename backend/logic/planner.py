from .models import Position, State, CellType
from typing import List, Set, Tuple
from .search_problem import SearchProblem
from dataclasses import replace


class RescueProblem(SearchProblem):
    def __init__(self, init: State, goal: Position, grid: list[list[CellType]],total_civilians: int,cost: dict = None):
        if cost is None:
            cost = {"move": 1, "rescue": 1}

        super().__init__(init, goal, cost)
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0
        self.total_civilians = total_civilians

    def isGoal(self, state: State) -> bool:
        traguardo = (state.robot_position == self.goal)
        all_civili = (len(state.saved_people) == self.total_civilians)
        return traguardo and all_civili

    def getSuccessors(self, state: State) -> list:
        successors = []

        if state.battery <= 0:
            return successors

        x = state.robot_position.x
        y = state.robot_position.y

        moves = {
            "su": Position(x, y - 1),
            "giù": Position(x, y + 1),
            "sinistra": Position(x - 1, y),
            "destra": Position(x + 1, y)
        }

        for action_name, new_pos in moves.items():
            if 0 <= new_pos.y < self.height and 0 <= new_pos.x < self.width:
                target_cell = self.grid[new_pos.y][new_pos.x]
                
                if target_cell != CellType.WALL:
                    
                    new_battery = state.battery
                    new_charges = state.extinguisher_charges
                    new_extinguished_fires = state.extinguished_fires
                    new_collected_extinguishers = state.collected_extinguishers
                    new_saved_people = state.saved_people
                    step_cost = self.cost.get("move", 1) 

                    #RACCOLTA ESTINTORE
                    if target_cell == CellType.EXTINGUISHER and new_pos not in new_collected_extinguishers:
                        new_charges += 1
                        new_collected_extinguishers = new_collected_extinguishers | frozenset([new_pos])
                        
                    # ATTRAVERSAMENTO FUOCO
                    elif target_cell == CellType.FIRE and new_pos not in new_extinguished_fires:
                        if new_charges > 0:
                            new_charges -= 1
                            new_extinguished_fires = new_extinguished_fires | frozenset([new_pos])
                        else:
                            step_cost = 10 
                    
                    # SALVATAGGIO CIVILE 
                    if target_cell == CellType.PERSON and new_pos not in new_saved_people:
                        new_saved_people = new_saved_people | frozenset([new_pos])
                        step_cost += self.cost.get("rescue", 1)

                    new_battery -= step_cost

                    new_state = replace(
                        state,
                        robot_position=new_pos,
                        battery=new_battery,
                        extinguisher_charges=new_charges,
                        saved_people=new_saved_people,
                        extinguished_fires=new_extinguished_fires,
                        collected_extinguishers=new_collected_extinguishers
                    )
                    
                    successors.append((action_name, new_state, step_cost))

        return successors


