from parser import parse_map
from planner import get_successors


mappa_test = [
    "#E#",
    "RFA",
    "###"
]

print(" TEST PARSER & PLANNER \n")

# 2. Testiamo il Parser
print("1️⃣ TRADUZIONE MAPPA (Parser)...")
try:
    grid, initial_state, goal_pos = parse_map(mappa_test, initial_battery=15)
    print("✅ Mappa tradotta con successo!")
    print(f"🤖 Posizione Iniziale Robot: ({initial_state.robot_position.x}, {initial_state.robot_position.y})")
    print(f"🏁 Posizione Arrivo: ({goal_pos.x}, {goal_pos.y})")
    print(f"🔋 Batteria di partenza: {initial_state.battery}\n")
except Exception as e:
    print(f"❌ Errore nel parser: {e}")
    exit()

# 3. Testiamo il Planner (Generazione Mosse)
print("2️⃣ LETTURA DEI FUTURI (Planner)...")
successors = get_successors(initial_state, grid, goal_pos)

print(f"Trovate {len(successors)} mosse valide dal punto di partenza:")
for action, state, cost in successors:
    print("-" * 30)
    print(f"AZIONE: {action}")
    print(f"Nuova posizione: ({state.robot_position.x}, {state.robot_position.y})")
    print(f"Batteria rimasta: {state.battery}")
    
    # Verifichiamo se il consumo di batteria è corretto per questa mossa
    consumo = initial_state.battery - state.battery
    if consumo == 10:
        print("ATTENZIONE: Il robot ha attraversato il fuoco senza estintore! (Costo: 10)")
    elif consumo == 1:
        print("Passo normale sul vuoto. (Costo: 1)")
    
    print(f"Costo percorso (g): {state.g}")
    print(f"Distanza stimata (h): {state.h}")
print("-" * 30)