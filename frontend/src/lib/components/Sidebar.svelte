<script>
    import GridDimensions from './GridDimensions.svelte';
    import ToolSelector from './ToolSelector.svelte';
    import ActionButtons from './ActionButtons.svelte';
    import LevelGrid from './LevelGrid.svelte';

    let {
        larghezza = $bindable(12),
        altezza = $bindable(10),
        strumentoAttivo = $bindable('Muro'),
        livelloAttivoId = $bindable(null),
        status = $bindable('🟢 Griglia pulita'),

        isPlaying = false,
        caricaLivello = () => {
        },
        nuovaGriglia = () => {
        },
        saveInLocalStorage = () => {
        },
        pythonSolve = () => {
        }
    } = $props();
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

    <ToolSelector bind:strumentoAttivo/>

    <ActionButtons
            bind:status
            {isPlaying}
            onClearGrid={nuovaGriglia}
            onSave={saveInLocalStorage}
            onSolve={pythonSolve}
    />
</aside>





