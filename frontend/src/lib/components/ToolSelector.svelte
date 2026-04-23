<script>
  import { strumenti } from '../constants.ts';

  export let strumentoAttivo = 'Muro';
</script>

<section class="flex-1">
  <h2 class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest mb-4">
    Seleziona gli strumenti per personalizzare lo scenario
  </h2>
  <div class="grid grid-cols-2 gap-3">
    {#each Object.entries(strumenti) as [id, data]}
      {#if id !== 'Vuoto'}
        <button
          onclick={() => strumentoAttivo = id}
          class="flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-all duration-200
          {strumentoAttivo === id
            ? `bg-zinc-800 ${data.activeClass} ring-4 shadow-lg scale-105`
            : 'border-zinc-800/50 bg-zinc-950 hover:bg-zinc-900'}">
          {#if data.img}
            <img src={data.img} class="w-10 h-10 mb-2 object-cover rounded-md [image-rendering:pixelated]" alt={id} />
          {:else}
            <span class="text-3xl mb-2 drop-shadow-md">{data.icon}</span>
          {/if}
          <span class="text-xs font-bold text-zinc-300">{id}</span>
          <span class="text-[10px] text-zinc-600 font-medium uppercase tracking-widest mt-0.5">{data.desc}</span>
        </button>
      {/if}
    {/each}
  </div>
</section>

