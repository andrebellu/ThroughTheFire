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
  export let caricaLivello = () => {};
  export let nuovaGriglia = () => {};
</script>

<aside class="w-80 shrink-0 h-full overflow-y-auto flex flex-col gap-6 bg-zinc-900/80 backdrop-blur-xl p-6 rounded-2xl border border-zinc-800 shadow-2xl">
  <GridDimensions bind:larghezza bind:altezza />

  <div class="h-px bg-zinc-800"></div>

  <LevelGrid
    bind:livelloAttivoId
    onCaricaLivello={caricaLivello}
    onNuovaGriglia={nuovaGriglia}
  />

  <div class="h-px bg-zinc-800"></div>

  <ToolSelector bind:strumentoAttivo />

  <ActionButtons
    bind:status
    onClearGrid={nuovaGriglia}
  />
</aside>





