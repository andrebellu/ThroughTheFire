from .models import CellType, Position, State
from typing import List, Tuple

SVELTE_TO_PYTHON = {
    'Muro': CellType.WALL,
    'Vuoto': CellType.EMPTY,
    'Fuoco': CellType.FIRE,
    'Civile': CellType.PERSON,
    'Robot': CellType.EMPTY,         # cella sotto il robot è vuota, la sua pos va nello stato
    'Extinguisher': CellType.EMPTY,  # !TODO da implementare logica
    'Arrivo': CellType.EMPTY         # !TODO da implementare logica
}

def parse_map(raw_map: List[str], initial_battery: int = 100, larghezza: int = None, altezza: int = None) -> Tuple[List[List[CellType]], State, Position]:
    grid = []           
    robot_pos = None    
    target_pos = None   

    for y in range(altezza):
        
        row = []
        
        for x in range(larghezza):
            idx = y * larghezza + x
            svelte_cell = raw_map[idx]
            
            pos= Position(x, y)
            if svelte_cell == "Robot":
                robot_pos = pos
            elif svelte_cell == 'Civile':
                target_pos = pos

            cell_type = SVELTE_TO_PYTHON.get(svelte_cell)
            row.append(cell_type)

        grid.append(row)

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