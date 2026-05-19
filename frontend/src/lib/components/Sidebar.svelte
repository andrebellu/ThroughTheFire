<script>
    import GridDimensions from './GridDimensions.svelte';
    import ToolSelector from './ToolSelector.svelte';
    import ActionButtons from './ActionButtons.svelte';
    import LevelGrid from './LevelGrid.svelte';

    export let larghezza = 12;
    export let altezza = 10;
    export let strumentoAttivo = 'Muro';
    export let livelloAttivoId = null;
    export let status = '🟢 Griglia pulita';
    export let caricaLivello = () => {
    };
    export let nuovaGriglia = () => {
    };
    export let saveInLocalStorage = () => {
    };
    export let pythonSolve = () => {
    };
    export let isPlaying = false;

    export let initialBattery = 100;
    export let initialOxygen = 100;
</script>

<aside class="w-80 shrink-0 h-full overflow-y-auto flex flex-col gap-6 bg-zinc-900/80 backdrop-blur-xl p-6 rounded-2xl border border-zinc-800 shadow-2xl">
    <GridDimensions bind:altezza bind:larghezza/>

    <div class="h-px bg-zinc-800"></div>

    <LevelGrid
            bind:livelloAttivoId
            onCaricaLivello={caricaLivello}
            onNuovaGriglia={nuovaGriglia}
    />

    <div class="h-px bg-zinc-800"></div>

    <div class="flex flex-col gap-4">
        <p class="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Parametri simulazione</p>

        <div class="flex flex-col gap-2">
            <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-zinc-400">🔋 Batteria iniziale</span>
                <span class="font-mono text-sm font-bold text-green-400">{initialBattery}</span>
            </div>
            <input
                    bind:value={initialBattery}
                    class="w-full h-2 rounded-full appearance-none cursor-pointer
                       bg-zinc-700 accent-green-500
                       disabled:opacity-40 disabled:cursor-not-allowed"
                    disabled={isPlaying}
                    max="500"
                    min="50"
                    step="10"
                    type="range"
            />
            <div class="flex justify-between text-xs text-zinc-600">
                <span>50</span>
                <span>500</span>
            </div>
        </div>

        <div class="flex flex-col gap-2">
            <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-zinc-400">💨 Ossigeno iniziale</span>
                <span class="font-mono text-sm font-bold text-blue-400">{initialOxygen}</span>
            </div>
            <input
                    bind:value={initialOxygen}
                    class="w-full h-2 rounded-full appearance-none cursor-pointer
                       bg-zinc-700 accent-blue-500
                       disabled:opacity-40 disabled:cursor-not-allowed"
                    disabled={isPlaying}
                    max="500"
                    min="50"
                    step="10"
                    type="range"
            />
            <div class="flex justify-between text-xs text-zinc-600">
                <span>50</span>
                <span>500</span>
            </div>
        </div>
    </div>

    <div class="h-px bg-zinc-800"></div>

    <ToolSelector bind:strumentoAttivo/>

    <ActionButtons
            bind:status
            {isPlaying}
            onClearGrid={nuovaGriglia}
            onSave={saveInLocalStorage}
            onSolve={pythonSolve}
    />
</aside>