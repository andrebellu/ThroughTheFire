# Through The Fire - Proposta di Progetto

**Candidati:** Andrea Bellu, Calvin You
**Corso:** Sistemi Intelligenti
**Anno Accademico:** 2025/2026

---

## Obiettivi del progetto
Il progetto *Through The Fire* si pone l'obiettivo di risolvere scenari fittizi di emergenza sfruttando algoritmi di ricerca. L'idea è quella di modellare un agente robotico di soccorso incaricato di salvare dei civili in un ambiente più o meno pericoloso.

## Struttura Concettuale

### Scenario
Il sistema distingue due tipologie di emergenza che influenzano il dominio:
* **Incendio**: presenza di fumo o fiamme che aumentano il costo di percorrenza o bloccano aree.
* **Terremoto**: crolli strutturali che obbligano il robot ad effettuare azioni fisiche di rimozione.

### Entità Dinamiche
* **Agente robotico**: caratterizzato da batteria limitata (percorso di andata e ritorno), capacità di trasporto limitata (numero massimo di civili trasportabili contemporaneamente) e gestione dell'ossigeno per le persone a bordo.
* **Civili**: entità da salvare con diverse priorità (feriti e illesi).

### Ambiente di simulazione
* **Mappe Standard**: livelli con difficoltà predefinita (*Peaceful, Easy, Normal, Hard, HardCore*).
* **Mappe Custom**: l'utente è libero di gestire la griglia inserendo ostacoli, muri e zone di fuoco a piacimento.

### Vincoli e Goal State
* **Vincoli**: gestione dell'ossigeno residuo per i civili e l'autonomia della batteria.
* **Goal State**: l'obiettivo dell'agente è portare tutti i civili in salvo entro un tempo massimo prestabilito.

---

## Azioni (Modellazione STRIPS)
* `Move`: spostamento tra celle adiacenti con consumo di batteria.
* `Rescue`: caricamento di un civile a bordo (precondizione: capacità residua > 0).
* `Clear Path`: rimozione delle macerie da una cella adiacente.
* `Extinguish`: spegnimento di un incendio (può richiedere una risorsa aggiuntiva come l'estintore).
* `Drop`: rilascio dei civili nel punto di raccolta (Goal state).

---

## Workflow
Il progetto segue un'architettura *Client-Server* per separare la logica di pianificazione dalla visualizzazione grafica:

### Frontend (Svelte)
* Consente la configurazione della mappa tramite editor visuale o scenari predefiniti.
* Genera un payload JSON con la topologia della griglia e lo stato iniziale delle entità.
* Riceve il piano d'azione dal backend e mostra i risultati tramite una simulazione in tempo reale.

### Backend (Python - FastAPI)
* Espone endpoint dedicati per la ricezione delle richieste di planning.
* **Parser**: traduce il JSON dal frontend e inizializza gli stati logici.
* **Solver**: trova il percorso ottimale tramite algoritmi di ricerca e una formula euristica custom (distanza di Manhattan pesata rispetto ai vincoli).

### Output e Analisi
* Il sistema restituisce il risultato e i dati sulle prestazioni dell'esecuzione (tempo, memoria, nodi).
* I dati vengono utilizzati per condurre un'analisi comportamentale dell'algoritmo al variare degli scenari.
