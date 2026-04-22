<script>
  import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
  import { Input } from "$lib/components/ui/input/index.js";

  let { status, onClearGrid, onSave} = $props();

  let name = $state('');

  function handleClear() {
    onClearGrid();
  }

  function handleSalva() {
    onSave();
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
    <AlertDialog.Root>
      <AlertDialog.Trigger>Save Custom Map</AlertDialog.Trigger>
      <AlertDialog.Content>
        <AlertDialog.Header>
          <AlertDialog.Title>Choose a name!</AlertDialog.Title>
          <AlertDialog.Description class="flex w-full items-center justify-center">
            <Input type="text" placeholder="name" class="w-full mt-2" bind:name />
          </AlertDialog.Description>
        </AlertDialog.Header>
        <AlertDialog.Footer>
          <AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
          <AlertDialog.Action>Continue</AlertDialog.Action>
        </AlertDialog.Footer>
      </AlertDialog.Content>
    </AlertDialog.Root>
  </button>
  <p class="text-center text-[10px] font-mono text-zinc-600 uppercase tracking-widest">{status}</p>
</div>

