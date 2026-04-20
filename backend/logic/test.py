from models import State, Position, CellType
from planner import get_successors

# 1. Creiamo una mini-mappa finta 3x3 per testare
# Mappa:
# [ R ] [  ] [ Muro ]
# [ Muro ] [ P ] [ Muro ]
# [   ] [   ] [ Goal ]
mock_grid = [
    [CellType.EMPTY, CellType.EMPTY, CellType.WALL],
    [CellType.WALL, CellType.PERSON, CellType.WALL],
    [CellType.EMPTY, CellType.EMPTY, CellType.GOAL]
]

# 2. Creiamo lo stato iniziale del robot (in alto a sinistra)
initial_state = State(
    robot_position=Position(0, 0),
    battery=10,
    saved_people=frozenset(),
    extinguished_fires=frozenset(),
    g=0,
    h=0
)

print("🤖 STATO INIZIALE:")
print(f"Posizione: ({initial_state.robot_position.x}, {initial_state.robot_position.y}) | Batteria: {initial_state.battery}")
print("-" * 40)

# 3. Chiamiamo la tua funzione!
successors = get_successors(initial_state, mock_grid)

# 4. Stampiamo i risultati per vedere se funziona
print(f"🔍 TROVATI {len(successors)} SUCCESSORI VALIDI:")
for action, state, cost in successors:
    print(f"✅ AZIONE: {action}")
    print(f"   -> Nuova Pos: ({state.robot_position.x}, {state.robot_position.y})")
    print(f"   -> Batteria residua: {state.battery}")
    print(f"   -> Costo (g): {state.g}")
    if state.saved_people:
        print(f"   -> 🎉 PERSONE SALVATE: {state.saved_people}")
    print("")