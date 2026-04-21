<script>
    import { schemaToMappa, coloriMinimap } from '../constants.ts';

    export let activeLevelId = null;
    export let onCaricaLivello = (level) => {};
    export let onNuovaGriglia = () => {};

    function caricaLivello(level) {
        activeLevelId = level.id;
        onCaricaLivello(level);
    }

    function nuovaGriglia() {
        activeLevelId = null;
        onNuovaGriglia();
    }

    const defaultLevels = [
        {
            id: 1,
            nome: 'Easy mode',
            difficolta: 'Facile',
            coloreDiff: '#34d399',
            larghezza: 12,
            altezza: 10,

            schema:
                `############
        #R.........#
        ##########.#
        #..........#
        #.##########
        #....F.....#
        ##########.#
        #..........#
        #.##########
        #........CA#`
        },
        {
            id: 2,
            difficolta: 'Medio',
            coloreDiff: '#facc15',   // yellow
            larghezza: 12,
            altezza: 10,

            schema:
                `############
#R.#.......#
#..#.#####.#
#..#.#...#.#
#..#.#.#.#.#
#....#.#.#.#
##.###.#.#.#
#..#F..#.C.#
#..####.##.#
#......#..A#`
        },
        {
            id: 3,
            difficolta: 'Difficile',
            coloreDiff: '#f87171',   // red
            larghezza: 12,
            altezza: 10,

            schema:
                `############
                #R.........#
                #..FF..FF..#
                #..........#
                #.FF....FF.#
                #..........#
                #..FF..FF..#
                #..........#
                #.FF....FF.#
                #.......CA.#`
        }
    ].map(l => ({...l, mappaPreview: schemaToMappa(l.schema)}));


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
        {#each defaultLevels as level}
            <button
                    onclick={() => caricaLivello(level)}
                    class="w-full flex items-center gap-3 p-3 rounded-xl border-2 transition-all duration-200 text-left
              {activeLevelId === level.id
                ? 'bg-zinc-800 border-orange-500/40 ring-1 ring-orange-500/20 shadow-lg shadow-orange-900/20'
                : 'border-zinc-800/50 bg-zinc-950 hover:bg-zinc-900 hover:border-zinc-700'}">


                <div
                        class="shrink-0 rounded-sm overflow-hidden border border-zinc-800/80"
                        style="display:grid;
                       grid-template-columns: repeat({level.larghezza}, 3px);
                       gap: 0.5px;
                       padding: 1px;
                       background: #18181b;">
                    {#each level.mappaPreview as cella}
                        <div style="width:3px; height:3px; background:{coloriMinimap[cella] ?? coloriMinimap.Vuoto};"></div>
                    {/each}
                </div>


                <div class="flex-1 min-w-0">
                    <div class="text-xs font-bold text-zinc-200 truncate">{level.nome}</div>
                    <div class="flex items-center gap-1.5 mt-0.5">
                  <span class="text-[10px] font-bold uppercase tracking-widest" style="color:{level.coloreDiff}">
                    {level.difficolta}
                  </span>
                        <span class="text-zinc-700">·</span>
                        <span class="text-[10px] font-mono text-zinc-600">{level.larghezza}×{level.altezza}</span>
                    </div>
                </div>


                {#if activeLevelId === level.id}
                    <span class="text-orange-400 text-xs shrink-0">✓</span>
                {:else}
                    <span class="text-zinc-700 text-xs shrink-0">→</span>
                {/if}
            </button>
        {/each}
    </div>
</section>