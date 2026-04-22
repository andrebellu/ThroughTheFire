<script>
  import Header from "./lib/components/Header.svelte";
  import Sidebar from "./lib/components/Sidebar.svelte";
  import MapGrid from "./lib/components/MapGrid.svelte";
  import { appState } from "$lib/runes.svelte.js";

  let larghezza = $state(12);
  let altezza   = $state(10);
  let strumentoAttivo = $state('Muro');
  let livelloAttivoId = $state(null);
  let status = $state('🟢 Griglia pulita');

  let mappa = $state([]);

  $effect.pre(() => {
    loadCustomMapsFromStorage();
  });

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
      localStorage.setItem(`custom_map_${name.trim()}`, JSON.stringify(toSave));
      status = `🟢 Mappa "${name.trim()}" salvata con successo!`;
      loadCustomMapsFromStorage();
    } catch (e) {
      status = '🔴 Errore nel salvataggio';
    }
  }

  function loadCustomMapsFromStorage() {
    const stored = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key.startsWith('custom_map_')) {
        try {
          const data = JSON.parse(localStorage.getItem(key));
          stored.push(data);
        } catch (e) {
          console.error('error');
        }
      }
    }
    appState.customMaps = stored;
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