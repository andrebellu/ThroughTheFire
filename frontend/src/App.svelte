<script>
  import Header from "./lib/components/Header.svelte";
  import Sidebar from "./lib/components/Sidebar.svelte";
  import MapGrid from "./lib/components/MapGrid.svelte";
  import {appState} from "$lib/runes.svelte.js";
  import {Toaster} from "$lib/components/ui/sonner/index.js";
  import {toast} from "svelte-sonner";

  const ENDPOINT = "http://localhost:8000/solve";
    let larghezza = $state(12);
    let altezza = $state(10);
    let strumentoAttivo = $state('Muro');
    let livelloAttivoId = $state(null);
    let status = $state('🟢 Griglia pulita');

    let plan = $state([]);
    let currentStep = $state(-1);
    let isPlataforma = $state(false);
    let mapSnapshot = $state([]);
    let isPlaying = $state(false);
    let playbackSpeed = $state(500);
    let robotPos = $state(-1);

    let planSteps = $state([]);

    function findRobotIndex(map) {
        return map.findIndex(c => c === 'Robot');
    }

    let mappa = $state([]);

    $effect.pre(() => {
        loadCustomMapsFromStorage();
    });

    $effect(() => {
        const nuovaDimensione = larghezza * altezza;
        if (mappa.length !== nuovaDimensione) {
            mappa = Array(nuovaDimensione).fill('Vuoto');
            livelloAttivoId = null;
        }
    });

    function caricaLivello(livello) {
        const expectedSize = livello.larghezza * livello.altezza;
        if (!Array.isArray(livello.mappaPreview) || livello.mappaPreview.length !== expectedSize) {
            toast.error("map not valid!")
            return;
        }

        larghezza = livello.larghezza;
        altezza = livello.altezza;
        mappa = [...livello.mappaPreview];
        livelloAttivoId = livello.id;
        status = `🟢 Livello caricato: ${livello.nome}`;

        toast.success("Map loaded");
    }

    function nuovaGriglia() {
        mappa = Array(larghezza * altezza).fill('Vuoto');
        livelloAttivoId = null;
        status = '🟢 Griglia pulita';

        toast.success("Grid cleaned");
    }

    function saveInLocalStorage(name) {
        if (!name || name.trim() === '') {
            toast.warning('Please enter a valid name!');
            return;
        }

        const toSave = {
            id: Date.now(),
            nome: name.trim(),
            larghezza,
            altezza,
            mappaPreview: [...mappa],
            createdAt: new Date().toISOString()
        };

        try {
            localStorage.setItem(`custom_map_${name.trim()}`, JSON.stringify(toSave));
            status = `Map "${name.trim()}" saved successfully.`;
            toast.success(status);
            loadCustomMapsFromStorage();
        } catch (e) {
            status = 'Error saving map!';
            toast.error(status);
        }
    }

    function loadCustomMapsFromStorage() {
        const stored = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith('custom_map_')) {
                try {
                    const data = JSON.parse(localStorage.getItem(key));
                    stored.push(data);
                } catch (e) {
                    console.error('error');
                }
            }
        }
        appState.customMaps = stored;
    }

    function runPlan() {
    }

    async function pythonSolve() {
        try {
            const resp = await fetch(ENDPOINT, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({w: larghezza, h: altezza, grid: mappa})
            });

            const data = await resp.json();

            if (data.success && Array.isArray(data.plan)) {
                planSteps = data.plan;
                const idx = findRobotIndex(mappa);
                robotPos = {index: idx !== -1 ? idx : 0};
                currentStep = -1;
                isPlaying = true;
                runPlan();
            } else {
                toast.error("No solution");
                planSteps = [];
            }
        } catch (e) {
            toast.error("Error connecting to solver.");
            console.error(e);
        }
    }

    planSteps = [
        {action: 'move', direction: 'right'},
        {action: 'move', direction: 'down'},
        {action: 'move', direction: 'down'},
        {action: 'move', direction: 'right'},
        {action: 'move', direction: 'up'},
        {action: 'move', direction: 'down'},
        {action: 'extinguish'}
    ]; // dati a caso per testare movimento robottino
</script>

<Toaster position="top-center"/>

<div class="h-screen w-full bg-zinc-950 text-zinc-100 flex flex-col font-sans selection:bg-orange-500/30">
    <Header/>

    <main class="flex-1 flex px-6 pb-6 gap-6 overflow-hidden">
        <Sidebar
                bind:altezza
                bind:larghezza
                bind:livelloAttivoId
                bind:status
                bind:strumentoAttivo
                {caricaLivello}
                {nuovaGriglia}
                {pythonSolve}
                {saveInLocalStorage}
        />
        <MapGrid
                bind:mappa
                {larghezza}
                {strumentoAttivo}
        />
    </main>
</div>