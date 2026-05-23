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
            'C': 'Civile', 'A': 'Arrivo', 'E': 'Extinguisher', '.': 'Vuoto', 'M': 'Macerie', 'P': 'Piccone'
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

<section class="space-y-2">
    <div class="flex items-center justify-between">
        <h2 class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest">Livelli</h2>
        <button
                class="text-[10px] text-zinc-500 hover:text-zinc-200 transition-colors uppercase tracking-widest font-bold px-2 py-0.5 rounded hover:bg-zinc-800"
                onclick={nuovaGriglia}>
            + Nuovo
        </button>
    </div>

    <div class="space-y-1">
        {#each levels as level}
            <button
                    onclick={() => caricaLivello(level)}
                    class="w-full flex items-center gap-2 px-2 py-1.5 rounded-lg border transition-all duration-150 text-left
                    {livelloAttivoId === level.id
                        ? 'bg-zinc-800 border-orange-500/50 shadow-md shadow-orange-900/20'
                        : 'border-transparent hover:bg-zinc-800/60 hover:border-zinc-700/50'}">

                <span
                        class="shrink-0 rounded-sm overflow-hidden border border-zinc-700/50"
                        style="display:grid;
                               grid-template-columns: repeat({level.larghezza}, 2px);
                               gap: 0.3px;
                               padding: 1px;
                               background: #18181b;">
                    {#each level.mappaPreview as cella}
                        <span style="width:2px; height:2px; background:{coloriMinimap[cella] ?? coloriMinimap.Vuoto};"></span>
                    {/each}
                </span>

                <span class="flex-1 min-w-0 flex items-center gap-2">
                    <span class="text-xs font-semibold text-zinc-200 truncate">{level.nome}</span>
                    <span class="text-[10px] font-bold uppercase tracking-wider shrink-0" style="color:{level.coloreDiff}">
                        {level.difficolta}
                    </span>
                </span>

                {#if livelloAttivoId === level.id}
                    <span class="text-orange-400 text-[10px] shrink-0">✓</span>
                {/if}
            </button>
        {/each}
    </div>

    {#if appState.customMaps.length > 0}
        <div class="h-px bg-zinc-800 my-1"></div>
        <p class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest">Custom</p>
        <div class="space-y-1">
            {#each appState.customMaps as customMap (customMap.id)}
                <button
                        onclick={() => caricaLivello(customMap)}
                        class="w-full flex items-center gap-2 px-2 py-1.5 rounded-lg border transition-all duration-150 text-left
                        {livelloAttivoId === customMap.id
                            ? 'bg-zinc-800 border-orange-500/50 shadow-md shadow-orange-900/20'
                            : 'border-transparent hover:bg-zinc-800/60 hover:border-zinc-700/50'}">

                    <span
                            class="shrink-0 rounded-sm overflow-hidden border border-zinc-700/50"
                            style="display:grid;
                                   grid-template-columns: repeat({customMap.larghezza}, 2px);
                                   gap: 0.3px;
                                   padding: 1px;
                                   background: #18181b;">
                        {#each customMap.mappaPreview as cella}
                            <span style="width:2px; height:2px; background:{coloriMinimap[cella] ?? coloriMinimap.Vuoto};"></span>
                        {/each}
                    </span>

                    <span class="flex-1 min-w-0 flex items-center gap-2">
                        <span class="text-xs font-semibold text-zinc-200 truncate">{customMap.nome}</span>
                        <span class="text-[10px] font-bold uppercase tracking-wider text-purple-400 shrink-0">Custom</span>
                    </span>

                    {#if livelloAttivoId === customMap.id}
                        <span class="text-orange-400 text-[10px] shrink-0">✓</span>
                    {/if}
                </button>
            {/each}
        </div>
    {/if}
</section>