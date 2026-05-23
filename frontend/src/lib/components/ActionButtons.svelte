<script>
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
    import {toast} from "svelte-sonner";
    import {Input} from "$lib/components/ui/input/index.js";

    let {status, onClearGrid, onSave, onSolve, isPlaying} = $props();
    let name = $state('');
    let dialogOpen = $state(false);

    function handleClear() {
        onClearGrid();
    }

    function handleSolve() {
        onSolve();
    }

    function handleSalva() {
        if (!name.trim()) {
            toast.warning('Please enter a valid name!');
            return;
        }
        onSave(name.trim());
        name = '';
        status = '🟢 Mappa salvata!';
    }
</script>

<div class="flex flex-col gap-2 pt-1">
    <div class="flex gap-2">
        <button
                class="flex-1 py-2.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-white text-xs font-black tracking-widest uppercase transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                disabled={isPlaying}
                onclick={handleClear}>
            Clear
        </button>

        <AlertDialog.Root onOpenChange={(open) => { dialogOpen = open; if (!open) name = ''; }} open={dialogOpen}>
            <AlertDialog.Trigger
                    class="flex-1 py-2.5 rounded-lg bg-orange-600 hover:bg-orange-500 text-white text-xs font-black tracking-widest uppercase transition-all active:scale-95">
                Save
            </AlertDialog.Trigger>
            <AlertDialog.Content>
                <AlertDialog.Header>
                    <AlertDialog.Title>Choose a name!</AlertDialog.Title>
                    <AlertDialog.Description class="flex w-full items-center justify-center">
                        <Input bind:value={name} class="w-full mt-2" placeholder="name" type="text"/>
                    </AlertDialog.Description>
                </AlertDialog.Header>
                <AlertDialog.Footer>
                    <AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
                    <AlertDialog.Action onclick={handleSalva}>Save</AlertDialog.Action>
                </AlertDialog.Footer>
            </AlertDialog.Content>
        </AlertDialog.Root>
    </div>

    <button
            class="w-full py-3 rounded-lg bg-green-700 hover:bg-green-600 text-white text-sm font-black tracking-widest uppercase shadow-[0_0_16px_rgba(34,197,94,0.15)] transition-all active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-none"
            disabled={isPlaying}
            onclick={handleSolve}>
        {#if isPlaying}
            ▶ Playing...
        {:else}
            Solve!
        {/if}
    </button>
</div>