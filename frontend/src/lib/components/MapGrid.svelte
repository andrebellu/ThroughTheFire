<script>
  import { strumenti } from '../constants.ts';

  export let mappa = [];
  export let larghezza = 12;
  export let strumentoAttivo = 'Muro';

  function coloraCella(indice) {
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
    evento.preventDefault();
    mappa[indice] = 'Vuoto';
  }
</script>

<section class="flex-1 h-full bg-zinc-900/30 rounded-2xl border border-zinc-800/50 flex flex-col items-center justify-center p-8 relative overflow-hidden">
  <!-- Sfondo punteggiato decorativo -->
  <div class="absolute inset-0 opacity-[0.03] pointer-events-none"
       style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 32px 32px;"></div>

  <!-- Griglia principale -->
  <div
    class="grid gap-1 p-3 bg-zinc-950 border border-zinc-800 rounded-xl shadow-2xl z-10"
    style="grid-template-columns: repeat({larghezza}, minmax(0, 1fr));">

    {#each mappa as tipoCella, indice}
      <button
        type="button"
        onclick={() => coloraCella(indice)}
        oncontextmenu={(e) => cancellaCella(e, indice)}
        onmouseenter={(e) => {
          if (e.buttons === 1) coloraCella(indice);
          if (e.buttons === 2) cancellaCella(e, indice);
        }}
        class="w-10 h-10 md:w-12 md:h-12 border border-zinc-800/80 rounded-md cursor-crosshair transition-all duration-100 flex items-center justify-center text-xl select-none hover:brightness-150 hover:scale-105 active:scale-95 p-0 {strumenti[tipoCella].color}"
        style="">

        {#if strumenti[tipoCella].img}
          <img src={strumenti[tipoCella].img} draggable="false"
            class="w-full h-full object-cover [image-rendering:pixelated]" alt={tipoCella} />
        {:else if strumenti[tipoCella].icon}
          <span class="flex items-center justify-center w-full h-full">{strumenti[tipoCella].icon}</span>
        {/if}
      </button>
    {/each}
  </div>

  <!-- Info dimensioni -->
  <div class="mt-6 text-zinc-600 font-mono text-xs font-bold tracking-widest uppercase">
    {larghezza}×{Math.ceil(mappa.length / larghezza)} Units // {mappa.length} Celle Totali
  </div>
</section>


