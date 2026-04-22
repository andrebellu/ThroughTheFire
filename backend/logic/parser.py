from models import CellType, Position, State
from typing import List, Tuple

def parse_map(raw_map: List[str], initial_battery: int = 100) -> Tuple[List[List[CellType]], State, Position]:
    
    char_to_cell = {
        '#': CellType.WALL,
        'F': CellType.FIRE,
        'C': CellType.PERSON,
        'A': CellType.GOAL,
        'E': CellType.EXTINGUISHER,
        '.': CellType.EMPTY
    }


    grid = []           
    robot_pos = None    
    target_pos = None   

    #Scanner mappa
    #y sarà il numero della riga (0, 1, 2...) e row sarà il testo (es: "#R......#").
    for y, row in enumerate(raw_map):
        
        grid_row = []
        
        # 'x' sarà la colonna (0, 1, 2...) e 'char' sarà la lettera (es: 'R').
        for x, char in enumerate(row):
            
            if char == 'R':
                robot_pos = Position(x, y)
                grid_row.append(CellType.EMPTY) 
                
            elif char == 'A':
                target_pos = Position(x, y)
                grid_row.append(CellType.GOAL)
                
            else:
                cell_type = char_to_cell.get(char, CellType.EMPTY)
                grid_row.append(cell_type)
                
        grid.append(grid_row)

    if robot_pos is None or target_pos is None:
        raise ValueError("ERRORE : La mappa è incompleta. Inserire il robot e il punto d'arrivo")

    
    initial_state = State(
        robot_position=robot_pos,
        battery=initial_battery,
        saved_people=frozenset(),           
        extinguished_fires=frozenset(),     
        collected_extinguishers=frozenset(),
        extinguisher_charges=0,             
        g=0,                                
        h=0                                 
    )

    return grid, initial_state, target_pos