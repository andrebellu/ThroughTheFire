<script>
  import { strumenti } from '../constants.ts';

  let { mappa, larghezza, strumentoAttivo = 'Muro', isPlaying = false, robotPos = -1, visitedCells = [] } = $props();

  let altezza = $derived(Math.max(1, Math.ceil(mappa.length / larghezza)));

  let boxW = $state(0);
  let boxH = $state(0);

  const GAP = 4;   
  const PAD = 12;  

  let cellSize = $derived.by(() => {
    if (boxW <= 0 || boxH <= 0) return 0;
    const availW = boxW - PAD * 2 - GAP * (larghezza - 1);
    const availH = boxH - PAD * 2 - GAP * (altezza - 1);
    const byW = availW / larghezza;
    const byH = availH / altezza;
    const size = Math.floor(Math.min(byW, byH));
    return size > 0 ? size : 0;
  });

  function misura(node) {
    const aggiorna = () => {
      const r = node.getBoundingClientRect();
      boxW = r.width;
      boxH = r.height;
    };
    aggiorna();
    const ro = new ResizeObserver(aggiorna);
    ro.observe(node);
    return { destroy() { ro.disconnect(); } };
  }

  function coloraCella(indice) {
    if (isPlaying) return;
    if (strumentoAttivo === 'Robot') {
      const old = mappa.findIndex(c => c === 'Robot');
      if (old !== -1) mappa[old] = 'Vuoto';
    }
    if (strumentoAttivo === 'Arrivo') {
      const old = mappa.findIndex(c => c === 'Arrivo');
      if (old !== -1) mappa[old] = 'Vuoto';
    }
    mappa[indice] = strumentoAttivo;
  }

  function cancellaCella(evento, indice) {
    if (isPlaying) return;
    evento.preventDefault();
    mappa[indice] = 'Vuoto';
  }

  function isVisited(indice) {
    return visitedCells.includes(indice);
  }
</script>

<section class="flex-1 min-h-0 w-full bg-zinc-900/30 rounded-2xl border border-zinc-800/50 flex flex-col items-center justify-center p-8 relative overflow-hidden">
  <div class="absolute inset-0 opacity-[0.03] pointer-events-none"
       style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 32px 32px;"></div>

  <div use:misura class="flex-1 min-h-0 w-full flex items-center justify-center z-10">
    {#if cellSize > 0}
      <div
        class="grid bg-zinc-950 border border-zinc-800 rounded-xl shadow-2xl"
        style="
          grid-template-columns: repeat({larghezza}, {cellSize}px);
          grid-template-rows: repeat({altezza}, {cellSize}px);
          gap: {GAP}px;
          padding: {PAD}px;
        ">
        {#each mappa as tipoCella, indice}
          <button
            type="button"
            onclick={() => coloraCella(indice)}
            oncontextmenu={(e) => cancellaCella(e, indice)}
            onmouseenter={(e) => {
              if (isPlaying) return;
              if (e.buttons === 1) coloraCella(indice);
              if (e.buttons === 2) cancellaCella(e, indice);
            }}
            disabled={isPlaying}
            class="relative border border-zinc-800/80 rounded-md cursor-crosshair transition-all duration-100 flex items-center justify-center select-none hover:brightness-150 hover:scale-105 active:scale-95 p-0 {strumenti[tipoCella].color} disabled:cursor-not-allowed"
            style="width: {cellSize}px; height: {cellSize}px;">
            {#if strumenti[tipoCella].img}
              <img
                src={strumenti[tipoCella].img}
                draggable="false"
                class="w-full h-full object-cover [image-rendering:pixelated]"
                alt={tipoCella}
              />
            {:else if strumenti[tipoCella].icon}
              <span class="flex items-center justify-center w-full h-full"
                    style="font-size: {Math.max(8, Math.floor(cellSize * 0.55))}px;">{strumenti[tipoCella].icon}</span>
            {/if}

            {#if isVisited(indice) && indice !== robotPos}
              <span class="absolute w-2 h-2 rounded-full bg-white shadow-[0_0_6px_rgba(255,255,255,0.8)]"></span>
            {/if}
          </button>
        {/each}
      </div>
    {/if}
  </div>

  <div class="mt-4 text-zinc-600 font-mono text-xs font-bold tracking-widest uppercase shrink-0">
    {larghezza}×{altezza} Units // {mappa.length} Celle Totali
  </div>
</section>