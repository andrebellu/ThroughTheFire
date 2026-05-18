from .models import CellType, Position, State
from typing import List, Tuple

SVELTE_TO_PYTHON = {
    'Muro': CellType.WALL,
    'Vuoto': CellType.EMPTY,
    'Fuoco': CellType.FIRE,
    'Civile': CellType.PERSON,
    'Robot': CellType.EMPTY,         
    'Extinguisher': CellType.EXTINGUISHER,
    'Arrivo': CellType.GOAL         
}


def parse_map(raw_map: List[str], initial_battery: int = 100, larghezza: int = None, altezza: int = None) -> Tuple[List[List[CellType]], State, Position, int]:
    if larghezza is None or altezza is None:
        raise ValueError("Dimensioni mappa mancanti")

    expected_len = larghezza * altezza
    if len(raw_map) != expected_len:
        raise ValueError(f"Dimensioni mappa non valide: attesi {expected_len} elementi, ricevuti {len(raw_map)}")

    grid = []
    exit_pos = None
    robot_pos = None
    civilians = set()

    for y in range(altezza):
        row = []

        for x in range(larghezza):
            idx = y * larghezza + x
            svelte_cell = raw_map[idx]

            pos = Position(x, y)
            if svelte_cell == "Robot":
                robot_pos = pos
            elif svelte_cell == 'Civile':
                civilians.add(pos)
            elif svelte_cell == 'Arrivo':
                exit_pos = pos

            cell_type = SVELTE_TO_PYTHON.get(svelte_cell)
            if cell_type is None:
                raise ValueError(f"Cella sconosciuta '{svelte_cell}' in posizione {x},{y}")
            row.append(cell_type)

        grid.append(row)

    if robot_pos is None or exit_pos is None:
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

    return grid, initial_state, exit_pos, len(civilians)