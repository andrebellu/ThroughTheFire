<script>
    import Header from "./lib/components/Header.svelte";
    import Sidebar from "./lib/components/Sidebar.svelte";
    import MapGrid from "./lib/components/MapGrid.svelte";
    import {appState} from "$lib/runes.svelte.js";
    import {Toaster} from "$lib/components/ui/sonner/index.js";
    import {toast} from "svelte-sonner";
    import PlaybackBar from "./lib/components/PlaybackBar.svelte";

    const ENDPOINT = "http://localhost:8000/solve";
    let larghezza = $state(12);
    let altezza = $state(10);
    let strumentoAttivo = $state('Muro');
    let livelloAttivoId = $state(null);
    let status = $state('🟢 Griglia pulita');
    let batteriaCorrente = $state(100);
    let batteryTrace = $state([]);
    let searchTimeMs = $state(0);

    let currentStep = $state(-1)
    let isPlaying = $state(false);
    let playbackSpeed = $state(500);
    let robotPos = $state(-1);
    let planSteps = $state([]);
    let visitedCells = $state([]);

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
        visitedCells = [];
        livelloAttivoId = livello.id;
        status = `🟢 Livello caricato: ${livello.nome}`;

        toast.success("Map loaded");
    }

    function nuovaGriglia() {
        mappa = Array(larghezza * altezza).fill('Vuoto');
        livelloAttivoId = null;
        status = '🟢 Griglia pulita';
        // clear visited trail
        visitedCells = [];

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

    function findRobotIndex(map) {
        return map.findIndex(c => c === 'Robot');
    }

    function executeStep(step) {
        if (!isPlaying || !step) {
            return;
        }

        if (step.action === 'move') {
            const dir = step.direction;
            let newPos = robotPos;

            if (dir === 'up') newPos -= larghezza;
            else if (dir === 'down') newPos += larghezza;
            else if (dir === 'left') newPos -= 1;
            else if (dir === 'right') newPos += 1;

            if (newPos >= 0 && newPos < mappa.length && mappa[newPos] !== 'Muro') {
                if (robotPos >= 0 && robotPos < mappa.length) {
                    // mark current cell as visited before moving
                    if (!visitedCells.includes(robotPos)) visitedCells = [...visitedCells, robotPos];
                    mappa[robotPos] = 'Vuoto';
                }
                mappa[newPos] = 'Robot';
                robotPos = newPos;
            }
        }

        currentStep += 1;

        if (Array.isArray(batteryTrace) && batteryTrace.length > currentStep) {
            batteriaCorrente = batteryTrace[currentStep];
        } else {
            if (step && step.action === 'move') {
                batteriaCorrente = Math.max(0, batteriaCorrente - 1);
            } else if (step && step.action === 'extinguish') {
                batteriaCorrente = Math.max(0, batteriaCorrente - 1);
            }
        }

        setTimeout(runPlan, playbackSpeed);
    }

    function runPlan() {
        if (!isPlaying) {
            return;
        }

        const nextIndex = currentStep + 1;

        if (nextIndex >= planSteps.length) {
            isPlaying = false;
            status = 'Plan completed!';
            toast.success(status);
            return;
        }

        const step = planSteps[nextIndex];
        executeStep(step);
    }

    function normalizeDirection(direction) {
        if (!direction) return null;
        const value = String(direction).trim().toLowerCase();
        if (value === 'up' || value === 'su') return 'up';
        if (value === 'down' || value === 'giu' || value === 'giu\u0300' || value === 'giù') return 'down';
        if (value === 'left' || value === 'sinistra') return 'left';
        if (value === 'right' || value === 'destra') return 'right';
        return null;
    }

    function normalizePlanSteps(rawSteps) {
        if (!Array.isArray(rawSteps)) return [];

        return rawSteps
            .map((step) => {
                if (typeof step === 'string') {
                    const dir = normalizeDirection(step);
                    return dir ? {action: 'move', direction: dir} : null;
                }

                if (step && typeof step === 'object') {
                    const action = String(step.action || '').trim().toLowerCase();
                    if (action === 'move') {
                        const dir = normalizeDirection(step.direction);
                        return dir ? {action: 'move', direction: dir} : null;
                    }
                    if (action === 'extinguish') {
                        return {action: 'extinguish'};
                    }
                }

                return null;
            })
            .filter(Boolean);
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
                planSteps = normalizePlanSteps(data.plan);

                batteryTrace = Array.isArray(data.battery_trace) ? data.battery_trace : [];
                searchTimeMs = typeof data.search_time_ms === 'number' ? data.search_time_ms : 0;

                if (typeof data.battery_start === 'number') {
                    batteriaCorrente = data.battery_start;
                } else if (typeof data.battery_remaining === 'number') {
                    batteriaCorrente = data.battery_remaining;
                }

                const idx = findRobotIndex(mappa);
                if (idx === -1) {
                    toast.error("No robot found on map.");
                    return;
                }
                if (planSteps.length === 0) {
                    toast.error("Plan format not supported.");
                    return;
                }

                robotPos = idx;
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
</script>

<Toaster position="top-center"/>

<div class="h-screen w-full bg-zinc-950 text-zinc-100 flex flex-col font-sans selection:bg-orange-500/30 overflow-hidden">
    <Header/>

    <main class="flex-1 min-h-0 flex px-6 pb-6 gap-6 overflow-hidden">
        <Sidebar
                bind:altezza
                bind:larghezza
                bind:livelloAttivoId
                bind:status
                bind:strumentoAttivo
                {caricaLivello}
                {isPlaying}
                {nuovaGriglia}
                {pythonSolve}
                {saveInLocalStorage}
        />
        <div class="flex-1 min-w-0 min-h-0 flex flex-col">
            <MapGrid
                    bind:mappa
                    {isPlaying}
                    {larghezza}
                    {robotPos}
                    {strumentoAttivo}
                    {visitedCells}
            />

            <PlaybackBar
                    {batteriaCorrente}
                    {searchTimeMs}
                    {status}
            />
        </div>
    </main>
</div>