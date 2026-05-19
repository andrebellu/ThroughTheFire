<script>
    import {strumenti} from '../constants.ts';

    export let strumentoAttivo = 'Muro';
</script>

<section>
    <h2 class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest mb-2">Strumenti</h2>
    <div class="grid grid-cols-3 gap-1.5">
        {#each Object.entries(strumenti) as [id, data]}
            {#if id !== 'Vuoto'}
                <button
                        onclick={() => strumentoAttivo = id}
                        class="flex flex-col items-center justify-center p-2 rounded-lg border transition-all duration-150
          {strumentoAttivo === id
            ? `bg-zinc-800 ${data.activeClass} ring-2 shadow-md`
            : 'border-zinc-800/50 bg-zinc-950 hover:bg-zinc-900 hover:border-zinc-700'}">
                    {#if data.img}
                        <img src={data.img} class="w-7 h-7 mb-1 object-cover rounded [image-rendering:pixelated]"
                             alt={id}/>
                    {:else}
                        <span class="text-xl mb-1">{data.icon}</span>
                    {/if}
                    <span class="text-[10px] font-bold text-zinc-300 leading-tight">{id}</span>
                </button>
            {/if}
        {/each}
    </div>
</section>