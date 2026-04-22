<script>
  import Header from "./lib/components/Header.svelte";
  import Sidebar from "./lib/components/Sidebar.svelte";
  import MapGrid from "./lib/components/MapGrid.svelte";

  let larghezza = $state(12);
  let altezza   = $state(10);
  let strumentoAttivo = $state('Muro');
  let livelloAttivoId = $state(null);
  let status = $state('🟢 Griglia pulita');

  let mappa = $state([]);

  $effect(() => {
    const nuovaDimensione = larghezza * altezza;
    if (mappa.length !== nuovaDimensione) {
      mappa = Array(nuovaDimensione).fill('Vuoto');
      livelloAttivoId = null;
    }
  });

  function caricaLivello(livello) {
    const expectedSize = livello.larghezza * livello.altezza;
    if (!Array.isArray(livello.mappaPreview) || livello.mappaPreview.length !== expectedSize) {
      status = '🔴 Livello non valido';
      return;
    }

    larghezza       = livello.larghezza;
    altezza         = livello.altezza;
    mappa           = [...livello.mappaPreview];
    livelloAttivoId = livello.id;
    status          = `🟢 Livello caricato: ${livello.nome}`;
  }

  function nuovaGriglia() {
    mappa           = Array(larghezza * altezza).fill('Vuoto');
    livelloAttivoId = null;
    status          = '🟢 Griglia pulita';
  }

  function saveInLocalStorage(name) {
    if (!name || name.trim() === '') {
      status = '🔴 Nome non valido';
      return;
    }

    const toSave = {
      id: Date.now(),
      nome: name.trim(),
      larghezza,
      altezza,
      mappaPreview: [...mappa],
      createdAt: new Date().toISOString()
    };

    try {
      console.log('Saving to localStorage:', toSave);
      localStorage.setItem(`custom_map_${name.trim()}`, JSON.stringify(toSave));
      status = `🟢 Mappa "${name.trim()}" salvata con successo!`;
    } catch (e) {
      status = '🔴 Errore nel salvataggio';
    }
  }
</script>


<div class="h-screen w-full bg-zinc-950 text-zinc-100 flex flex-col font-sans selection:bg-orange-500/30">
  <Header />

  <main class="flex-1 flex px-6 pb-6 gap-6 overflow-hidden">
    <Sidebar
      bind:larghezza
      bind:altezza
      bind:strumentoAttivo
      bind:livelloAttivoId
      bind:status
      {caricaLivello}
      {nuovaGriglia}
      {saveInLocalStorage}
    />
    <MapGrid
      bind:mappa
      {larghezza}
      {strumentoAttivo}
    />
  </main>
</div>