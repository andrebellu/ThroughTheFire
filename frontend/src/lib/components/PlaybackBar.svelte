<script>
    let {
        batteriaCorrente = 100,
        ossigenoCorrente = 100,
        oxygenActive = false,
        searchTimeMs = 0,
        status = 'In attesa'
    } = $props();

    const battColore = $derived(batteriaCorrente > 20 ? 'text-green-500' : 'text-red-500');
    const battBarra  = $derived(batteriaCorrente > 20 ? 'bg-green-500' : 'bg-red-500');
    const oxyColore  = $derived(ossigenoCorrente > 20 ? 'text-blue-400' : 'text-red-500');
    const oxyBarra   = $derived(ossigenoCorrente > 20 ? 'bg-blue-400' : 'bg-red-500');
</script>

<div class="mt-4 bg-zinc-900 border border-zinc-800 p-4 rounded-xl flex items-center justify-between shrink-0 flex-wrap gap-4">

    <div class="flex items-center gap-6">
        <div class="flex gap-2 opacity-30">
            <div class="bg-zinc-800 px-3 py-1 rounded text-sm">⏪</div>
            <div class="bg-zinc-800 px-3 py-1 rounded text-sm">▶️</div>
            <div class="bg-zinc-800 px-3 py-1 rounded text-sm">⏩</div>
        </div>

        <div class="w-px h-6 bg-zinc-700"></div>

        <div class="text-sm font-semibold text-zinc-300">
            {status}
        </div>
    </div>

    <div class="flex items-center gap-4 flex-wrap">

        <span class="text-xs font-semibold text-zinc-500 uppercase tracking-wider">
            Solve {searchTimeMs.toFixed(1)} ms
        </span>

        <div class="w-px h-6 bg-zinc-700"></div>

        <div class="flex items-center gap-3">
            <span class="text-sm font-bold text-zinc-500 uppercase tracking-wider">Batteria</span>
            <div class="w-32 h-3 bg-zinc-950 rounded-full overflow-hidden border border-zinc-800">
                <div
                    class="h-full transition-all duration-300 {battBarra}"
                    style="width: {batteriaCorrente}%;"
                ></div>
            </div>
            <span class="font-mono text-lg font-bold w-12 text-right {battColore}">
                {batteriaCorrente}%
            </span>
        </div>

        <div class="w-px h-6 bg-zinc-700"></div>

        <div class="flex items-center gap-3 transition-opacity duration-500 {oxygenActive ? 'opacity-100' : 'opacity-30'}">
            <span class="text-sm font-bold text-zinc-500 uppercase tracking-wider">Ossigeno</span>
            <div class="w-32 h-3 bg-zinc-950 rounded-full overflow-hidden border border-zinc-800">
                <div
                    class="h-full transition-all duration-300 {oxyBarra}"
                    style="width: {ossigenoCorrente}%;"
                ></div>
            </div>
            <span class="font-mono text-lg font-bold w-12 text-right {oxyColore}">
                {oxygenActive ? `${ossigenoCorrente}%` : '--'}
            </span>
        </div>

    </div>
</div>