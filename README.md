# Through The Fire

**Autori:** Andrea Bellu, Calvin You  
**Corso:** Sistemi Intelligenti  
**Anno Accademico:** 2025/2026  
**Università:** Università degli Studi di Brescia

![](https://github.com/andrebellu/ThroughTheFire/blob/master/dashboard.png)

---

## Descrizione del Progetto
**Through the Fire** è un'applicazione web interattiva focalizzata sulla pianificazione deterministica di un agente autonomo in scenari di emergenza. 

Il sistema simula un robot di soccorso che deve navigare all'interno di una mappa per trovare e salvare dei civili intrappolati, per poi condurli verso l'uscita. L'ambiente è ostile: il robot è limitato da **batteria** (che si consuma muovendosi o attraversando pericoli) e **ossigeno** (che si consuma progressivamente in base al numero di civili soccorsi). 

Il cuore logico del progetto è un motore decisionale basato su **Weighted A*** associato a un'euristica ammissibile custom (Distanza di Manhattan multi-obiettivo). L'algoritmo non cerca solo la via d'uscita, ma risolve simultaneamente il problema del salvataggio dei civili (variante TSP) e l'ottimizzazione delle risorse (raccolta estintori e distruzione ostacoli).

## Stack Tecnologico
Il progetto adotta un'architettura disaccoppiata Client-Server:
* **Frontend:** Svelte 5 (Vite) - gestisce l'editor interattivo della mappa, la serializzazione dello scenario e il rendering reattivo (senza Virtual DOM) delle animazioni.
* **Backend:** Python 3 (FastAPI + Uvicorn) - riceve lo stato iniziale, istanzia lo spazio degli stati immutabile ed esegue l'algoritmo di ricerca per trovare il piano d'azione ottimale.

---

## Guida all'Installazione e Avvio

Il progetto richiede l'avvio separato dei due ambienti (Frontend e Backend). Assicurati di avere installati **Node.js** (npm) e **Python 3.10+**.

### 1. Avvio del Backend (Python)
Apri un terminale e posizionati nella cartella `backend`:

```bash
cd backend
```
Crea e attiva un ambiente virtuale (consigliato):
```Bash

# Su Windows:
python -m venv .venv
.venv\Scripts\activate

# Su macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate
```
Installa le dipendenze:
```Bash

pip install -r requirements.txt
```

Tornare nella cartella principale del progetto e avviare il server FastAPI tramite Uvicorn:
```Bash

# Il server partirà di default su [http://127.0.0.1:8000](http://127.0.0.1:8000)
cd ..
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
### 2. Avvio del Frontend (Svelte)

Apri un nuovo terminale e posizionati nella cartella frontend:
```Bash

cd frontend
```
Installa i pacchetti Node:
```Bash

npm install
```
Avvia il server di sviluppo Vite:
```bash

# Il client partirà di default su http://localhost:5173
npm run dev
```
Una volta avviati entrambi i server, apri il browser all'indirizzo del frontend per utilizzare l'applicazione.
## Funzionalità Principali

- Custom Level Editor: disegna la tua mappa piazzando Muri, Fuoco, Civili, Estintori e Macerie. Le mappe create posso essere salvate nel LocalStorage del tuo browser cliccando il tasto "Salva".

- Livelli Benchmark: 5 livelli predefiniti (da Easy a Nightmare) per testare le prestazioni e la scalabilità dell'algoritmo.

- Gestione Risorse:

  - Batteria: decrementa a ogni passo. Attraversare il fuoco senza estintore costa molto di più di un passo normale.

  - Ossigeno: inizia a consumarsi solo dopo aver recuperato il primo civile (introduce un vincolo temporale).

- Motore di Animazione: sincronizzazione visiva del piano calcolato dal backend.

## L'Algoritmo (Weighted A*)

L'algoritmo risolutivo affronta il fenomeno della State Space Explosion causato dalle molteplici variabili (civili, fuochi, estintori) attraverso:

- Stati Immutabili (Frozen Dataclasses): per bloccare la re-immissione di nodi identici nella coda di priorità.

- Euristica Custom Multi-Target: stima il costo prendendo il civile "più distante" (massimizzando il lower-bound pur restando ammissibile).

- Pesi Euristici (W=2): sacrifica la garanzia dell'ottimalità assoluta in favore di tempi di calcolo real-time, evitando timeout computazionali (impostato a max 25 secondi) su mappe complesse.
