<script>
    export let larghezza = 12;
    export let altezza = 10;
</script>

<section class="space-y-2">
    <h2 class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest">Dimensioni Griglia</h2>
    <div class="flex gap-2">
        <label class="flex-1 flex items-center gap-2 bg-zinc-950 px-3 py-2 rounded-lg border border-zinc-800 focus-within:border-orange-500/50 transition-colors">
            <span class="text-[10px] text-zinc-500 uppercase font-bold shrink-0">W</span>
            <input
                    bind:value={larghezza}
                    class="w-full bg-transparent text-orange-400 font-mono text-sm font-bold outline-none"
                    max="30"
                    min="5"
                    type="number"
            />
        </label>
        <label class="flex-1 flex items-center gap-2 bg-zinc-950 px-3 py-2 rounded-lg border border-zinc-800 focus-within:border-orange-500/50 transition-colors">
            <span class="text-[10px] text-zinc-500 uppercase font-bold shrink-0">H</span>
            <input
                    bind:value={altezza}
                    class="w-full bg-transparent text-orange-400 font-mono text-sm font-bold outline-none"
                    max="30"
                    min="5"
                    type="number"
            />
        </label>
    </div>
</section>