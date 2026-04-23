<script>
  export let larghezza = 12;
  export let altezza = 10;
</script>

<section class="space-y-3">
  <h2 class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest">Dimensioni Griglia</h2>
  <div class="flex gap-3">
    <label class="flex-1 bg-zinc-950 p-3 rounded-xl border border-zinc-800 focus-within:border-orange-500/50 transition-colors">
      <span class="block text-[10px] text-zinc-500 uppercase font-bold mb-1">Larghezza</span>
      <input
        type="number"
        min="5"
        max="30"
        bind:value={larghezza}
        class="w-full bg-transparent text-orange-400 font-mono text-xl font-bold outline-none"
      />
    </label>
    <label class="flex-1 bg-zinc-950 p-3 rounded-xl border border-zinc-800 focus-within:border-orange-500/50 transition-colors">
      <span class="block text-[10px] text-zinc-500 uppercase font-bold mb-1">Altezza</span>
      <input
        type="number"
        min="5"
        max="30"
        bind:value={altezza}
        class="w-full bg-transparent text-orange-400 font-mono text-xl font-bold outline-none"
      />
    </label>
  </div>
</section>


