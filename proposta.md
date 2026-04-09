# Proposte Progetto

- Disaster Management: evacuazione intelligente
    - Scenario: terremoto, incendio o altre emergenze che rendono alcune aree inaccessibili o pericolose.
    - Obiettivo: un robot di soccorso deve raggiungere le persone, raccoglierle e portarle in una zona sicura.
    - Vincoli del robot:
        - batteria limitata
        - capacità massima di trasporto di persone
    - Ambiente di prova: 
        - mappa di un edificio con 5 livelli di difficoltà crescente
        - oppure mappa custom definita dall'utente
    - Algoritmi di ricerca:
        - A* o IDA*
        - eventuale confronto con altre strategie già disponibili, adattate al caso d'uso
    - Euristica:
        - funzione custom che tenga conto di distanza, numero di persone, batteria residua, ossigeno e aree bloccate
    - Possibili estensioni:
        - ossigeno limitato per le persone trasportate
        - più robot che collaborano tra loro
        - priorità diverse per le persone da salvare
        - ostacoli dinamici che cambiano durante la simulazione
        - simulazione di tempo di percorrenza e consumo energetico
    - Interfaccia grafica:
        - visualizzazione con pygame oppure svelte
        - comunicazione con il backend tramite endpoint dedicati

- Giochino con qualche feature particolare
