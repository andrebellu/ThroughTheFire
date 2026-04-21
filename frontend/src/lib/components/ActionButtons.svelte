<script>
  export let status = '🟢 Griglia pulita';
  export let onClearGrid = () => {};
  export let onSalva = () => {};

  function handleClear() {
    onClearGrid();
  }

  function handleSalva() {
    onSalva();
  }

</script>

<div class="mt-auto pt-2 space-y-3">
  <button
    onclick={handleClear}
    class="w-full py-4 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-white font-black tracking-widest uppercase shadow-[0_0_20px_rgba(255,255,255,0.1)] transition-all active:scale-95">
    Clear Grid
    </button>
  <button
    onclick={handleSalva}
    class="w-full py-4 rounded-xl bg-orange-600 hover:bg-orange-500 text-white font-black tracking-widest uppercase shadow-[0_0_20px_rgba(234,88,12,0.3)] transition-all active:scale-95">
    Salva in Database
  </button>
  <p class="text-center text-[10px] font-mono text-zinc-600 uppercase tracking-widest">{status}</p>
</div>

