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
        console.log('handleSalva called with name:', name);
        if (!name.trim()) {
            toast.warning('Please enter a valid name!');
            return;
        }
        console.log('Calling onSave with:', name.trim());
        onSave(name.trim());
        name = '';
        status = '🟢 Mappa salvata!';
    }

</script>

<div class="flex flex-col gap-2">
    <div class="mt-auto pt-2 flex flex-row gap-x-2">
        <button
                class="w-1/2 h-16 py-4 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-white font-black tracking-widest uppercase transition-all disabled:scale-95 disabled:cursor-not-allowed disabled:bg-zinc-900/50 disabled:shadow-none"
                disabled={isPlaying}
                onclick={() => {
                    handleClear();
                }}>
            Clear Grid
        </button>

        <AlertDialog.Root onOpenChange={(open) => {
            dialogOpen = open;
            if (!open) name = '';
        }} open={dialogOpen}>
            <AlertDialog.Trigger
                    class="w-1/2 h-16 py-4 rounded-xl bg-orange-600 hover:bg-orange-500 text-white font-black tracking-widest uppercase transition-all active:scale-95 disabled:scale-95! disabled:cursor-not-allowed! disabled:bg-zinc-900/50! disabled:shadow-none!">
                Save Map
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
                    <AlertDialog.Action onclick={() => {
                        handleSalva();
                    }}>Save
                    </AlertDialog.Action>
                </AlertDialog.Footer>
            </AlertDialog.Content>
        </AlertDialog.Root>
    </div>

    <button
            class="w-full py-4 rounded-xl bg-green-800 hover:bg-green-700 text-white font-black tracking-widest uppercase shadow-[0_0_20px_rgba(255,255,255,0.1)] transition-all active:scale-95 disabled:scale-95 disabled:cursor-not-allowed disabled:bg-zinc-900/50 disabled:shadow-none"
            disabled={isPlaying}
            onclick={handleSolve}
    >
        {#if isPlaying}
            Playing...
        {:else}
            Solve!
        {/if}
    </button>
</div>
