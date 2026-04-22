<script lang="ts">
    import { coloriMinimap, defaultLevels } from '../constants';
    import { appState } from "$lib/runes.svelte.js";

    export let livelloAttivoId = null;
    export let onCaricaLivello = (_) => {};
    export let onNuovaGriglia = () => {};

    function caricaLivello(level) {
        livelloAttivoId = level.id;
        onCaricaLivello(level);
    }

    function nuovaGriglia() {
        livelloAttivoId = null;
        onNuovaGriglia();
    }

    function schemaToMappa(schema: string) {
        const charMap: Record<string, string> = {
            '#': 'Muro', 'R': 'Robot', 'F': 'Fuoco',
            'C': 'Civile', 'A': 'Arrivo', 'E': 'Extinguisher', '.': 'Vuoto'
        };
        return schema
            .trim()
            .split('\n')
            .map(riga => riga.trim())
            .filter(riga => riga.length > 0)
            .flatMap(riga => riga.split('').map(c => charMap[c] ?? 'Vuoto'));
    }

    const levels = defaultLevels.map(l => ({...l, mappaPreview: schemaToMappa(l.schema)}));
</script>

<section class="space-y-3">
    <div class="flex items-center justify-between">
        <h2 class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest">Default Levels</h2>
        <button
                class="text-[10px] text-zinc-500 hover:text-zinc-200 transition-colors uppercase tracking-widest font-bold px-2 py-1 rounded-md hover:bg-zinc-800 border border-transparent hover:border-zinc-700"
                onclick={nuovaGriglia}>
            + Nuovo
        </button>
    </div>

    <div class="space-y-2">
        {#each levels as level}
            <button
                    onclick={() => caricaLivello(level)}
                    class="w-full flex items-center gap-3 p-3 rounded-xl border-2 transition-all duration-200 text-left
              {livelloAttivoId === level.id
                ? 'bg-zinc-800 border-orange-500/40 ring-1 ring-orange-500/20 shadow-lg shadow-orange-900/20'
                : 'border-zinc-800/50 bg-zinc-950 hover:bg-zinc-900 hover:border-zinc-700'}">

                <span
                        class="shrink-0 rounded-sm overflow-hidden border border-zinc-800/80"
                        style="display:grid;
                       grid-template-columns: repeat({level.larghezza}, 3px);
                       gap: 0.5px;
                       padding: 1px;
                       background: #18181b;">
                    {#each level.mappaPreview as cella}
                        <span style="width:3px; height:3px; background:{coloriMinimap[cella] ?? coloriMinimap.Vuoto};"></span>
                    {/each}
                </span>

                <span class="flex-1 min-w-0 block">
                    <span class="text-xs font-bold text-zinc-200 truncate block">{level.nome}</span>
                    <span class="flex items-center gap-1.5 mt-0.5">
                  <span class="text-[10px] font-bold uppercase tracking-widest" style="color:{level.coloreDiff}">
                    {level.difficolta}
                  </span>
                        <span class="text-zinc-700">·</span>
                        <span class="text-[10px] font-mono text-zinc-600">{level.larghezza}×{level.altezza}</span>
                    </span>
                </span>

                {#if livelloAttivoId === level.id}
                    <span class="text-orange-400 text-xs shrink-0">✓</span>
                {:else}
                    <span class="text-zinc-700 text-xs shrink-0">→</span>
                {/if}
            </button>
        {/each}
    </div>

    {#if appState.customMaps.length > 0}
        <div class="h-px bg-zinc-800 mt-4"></div>

        <h2 class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest">Custom Maps</h2>
        <div class="space-y-2">
            {#each appState.customMaps as customMap (customMap.id)}
                <button
                        onclick={() => caricaLivello(customMap)}
                        class="w-full flex items-center gap-3 p-3 rounded-xl border-2 transition-all duration-200 text-left
                  {livelloAttivoId === customMap.id
                    ? 'bg-zinc-800 border-orange-500/40 ring-1 ring-orange-500/20 shadow-lg shadow-orange-900/20'
                    : 'border-zinc-800/50 bg-zinc-950 hover:bg-zinc-900 hover:border-zinc-700'}">

                    <span
                            class="shrink-0 rounded-sm overflow-hidden border border-zinc-800/80"
                            style="display:grid;
                           grid-template-columns: repeat({customMap.larghezza}, 3px);
                           gap: 0.5px;
                           padding: 1px;
                           background: #18181b;">
                        {#each customMap.mappaPreview as cella}
                            <span style="width:3px; height:3px; background:{coloriMinimap[cella] ?? coloriMinimap.Vuoto};"></span>
                        {/each}
                    </span>

                    <span class="flex-1 min-w-0 block">
                        <span class="text-xs font-bold text-zinc-200 truncate block">{customMap.nome}</span>
                        <span class="flex items-center gap-1.5 mt-0.5">
                      <span class="text-[10px] font-bold uppercase tracking-widest text-purple-400">
                        Custom
                      </span>
                            <span class="text-zinc-700">·</span>
                            <span class="text-[10px] font-mono text-zinc-600">{customMap.larghezza}×{customMap.altezza}</span>
                        </span>
                    </span>

                    {#if livelloAttivoId === customMap.id}
                        <span class="text-orange-400 text-xs shrink-0">✓</span>
                    {:else}
                        <span class="text-zinc-700 text-xs shrink-0">→</span>
                    {/if}
                </button>
            {/each}
        </div>
    {/if}
</section>