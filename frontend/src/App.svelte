<script>
  // ==========================================================================
  // (Logica e stati)
  // ==========================================================================

  // $state:  Se cambiano, lo schermo si aggiorna.
  let larghezza = $state(12);
  let altezza = $state(10);
  let strumentoAttivo = $state('Muro');
  let status = $state('🟢 Pronto');
  
  // Array principale della mappa. Crea una lista lunga (larghezza * altezza) 
  // e la riempie di parole 'Vuoto'.
  let mappa = $state(Array(larghezza * altezza).fill('Vuoto'));

  // $derived: Variabile matematica autonoma. Ricalcola le celle totali 
  // solo quando larghezza o altezza vengono modificate dall'utente.
  let totaleCelle = $derived(larghezza * altezza);

  // $effect: Il guardiano di sistema. Controlla continuamente la logica.
  $effect(() => {
    const nuovaDimensione = larghezza * altezza;
    // Se l'utente ha cambiato le dimensioni, l'array attuale è vecchio.
    // Buttalo via e creane uno nuovo pulito.
    if (mappa.length !== nuovaDimensione) {
      mappa = Array(nuovaDimensione).fill('Vuoto');
    }
  });

  // DIZIONARIO STRUMENTI: Contiene tutti i dati visivi per ogni blocco.
  // Usiamo 'img' per percorsi di file reali e 'icon' per le emoji.
  const strumenti = {
    'Muro': { img: '/Stone.jpg', desc: 'Blocca', color: 'bg-zinc-700', activeClass: 'ring-zinc-400/30' },
    'Fuoco': { icon: '🔥', desc: 'Pericolo', color: 'bg-orange-900', activeClass: 'border-orange-500 ring-orange-500/30' },
    'Robot': { img: 'Robot.png', desc: 'Start', color: 'bg-blue-900', activeClass: 'border-blue-500 ring-blue-500/30' },
    'Civile': { icon: '🧑', desc: 'Target', color: 'bg-emerald-900', activeClass: 'border-emerald-500 ring-emerald-500/30' },
    'Arrivo': { icon: '🏁', desc: 'Finish Point', color: 'bg-emerald-900', activeClass: 'border-emerald-500 ring-emerald-500/30' },
    'Vuoto': { icon: '', desc: 'Semplice cella', color: 'bg-zinc-800/50', activeClass: '' }
  };

  // Funzione per "Dipingere" sulla griglia
  function coloraCella(indice) {
    // Limite di 1 solo Robot
    if (strumentoAttivo === 'Robot') {
      // Si cerca nell'array se esiste già un 'Robot'.
      // findIndex restituisce il numero della cella (es. 42), oppure -1 se non c'è.
      const posizioneVecchioRobot = mappa.findIndex(cella => cella === 'Robot');
      // 2. Se ha trovato un vecchio robot (posizione diversa da -1)...
      if (posizioneVecchioRobot !== -1) {
        // ...lo cancella, facendolo tornare 'Vuoto'
        mappa[posizioneVecchioRobot] = 'Vuoto';
      }
    }
    // Limite di 1 solo Punto di Arrivo 
    if (strumentoAttivo === 'Arrivo') {
      // Si cerca se esiste già una cella chiamata 'Arrivo'
      const posizioneVecchioArrivo = mappa.findIndex(cella => cella === 'Arrivo');
      
      // Se lo si trova, lo cancella trasformandolo in 'Vuoto'
      if (posizioneVecchioArrivo !== -1) {
        mappa[posizioneVecchioArrivo] = 'Vuoto';
      }
    }
    // Piazza lo strumento selezionato nella nuova cella cliccata
    mappa[indice] = strumentoAttivo;
}

  function cancellaCella(evento, indice) {
    // 1. preventDefault() è FONDAMENTALE. Impedisce al browser di aprire
    // la classica tendina grigia di Windows/Mac ("Copia", "Incolla", "Salva come...")
    evento.preventDefault(); 
    
    // 2. Riporta semplicemente la cella allo stato originale
    mappa[indice] = 'Vuoto';
}








</script>
<div class="h-screen w-full bg-zinc-950 text-zinc-100 flex flex-col font-sans selection:bg-orange-500/30">

  <header class="shrink-0 w-full py-6 flex flex-col items-center justify-center">
    <h1 class="text-orange-500 font-black text-4xl tracking-tighter uppercase italic leading-none drop-shadow-[0_0_15px_rgba(249,115,22,0.4)]">THROUGH THE FIRE</h1>
  </header>

  <main class="flex-1 flex px-6 pb-6 gap-6 overflow-hidden">

    <aside class="w-80 shrink-0 h-full overflow-y-auto flex flex-col gap-8 bg-zinc-900/80 backdrop-blur-xl p-6 rounded-2xl border border-zinc-800 shadow-2xl">
      
      <section class="space-y-4">
        <h2 class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest">Dimensioni Griglia</h2>
        <div class="flex gap-4">
          
          <label class="flex-1 bg-zinc-950 p-3 rounded-xl border border-zinc-800 focus-within:border-orange-500/50 transition-colors">
            <span class="block text-[10px] text-zinc-500 uppercase font-bold mb-1">Larghezza</span>
            <input type="number" min="5" max="30" bind:value={larghezza} class="w-full bg-transparent text-orange-400 font-mono text-xl font-bold outline-none" />
          </label>
          
          <label class="flex-1 bg-zinc-950 p-3 rounded-xl border border-zinc-800 focus-within:border-orange-500/50 transition-colors">
            <span class="block text-[10px] text-zinc-500 uppercase font-bold mb-1">Altezza</span>
            <input type="number" min="5" max="30" bind:value={altezza} class="w-full bg-transparent text-orange-400 font-mono text-xl font-bold outline-none" />
          </label>
        </div>
      </section>

      <section class="flex-1">
        <h2 class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest mb-4">Seleziona gli strumenti per personalizzare lo scenario</h2>
        
        <div class="grid grid-cols-2 gap-3">
          
          {#each Object.entries(strumenti) as [id, data]}
            {#if id !== 'Vuoto'}
              
              <button 
              onclick={() => strumentoAttivo = id}
              class="flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-all duration-200
              {strumentoAttivo === id ? `bg-zinc-800 ${data.activeClass} ring-4 shadow-lg scale-105` : 'border-zinc-800/50 bg-zinc-950 hover:bg-zinc-900'}">
              
                {#if data.img}
                    <img src={data.img} class="w-10 h-10 mb-2 object-cover rounded-md [image-rendering:pixelated]" alt={id} />
                {:else}
                    <span class="text-3xl mb-2 drop-shadow-md">{data.icon}</span>
                {/if}
                
                <span class="text-xs font-bold text-zinc-300">{id}</span>
                <span class="text-[10px] text-zinc-600 font-medium uppercase tracking-widest mt-0.5">{data.desc}</span>
              </button>
            {/if}
          {/each}
          
        </div>
      </section>

      <div class="mt-auto pt-4">
        <button class="w-full py-4 rounded-xl bg-orange-600 hover:bg-orange-500 text-white font-black tracking-widest uppercase shadow-[0_0_20px_rgba(234,88,12,0.3)] transition-all active:scale-95">
          Salva in Database
        </button>
        <p class="text-center text-[10px] font-mono text-zinc-600 uppercase tracking-widest mt-4">{status}</p>
      </div>
    </aside>

    <section class="flex-1 h-full bg-zinc-900/30 rounded-2xl border border-zinc-800/50 flex flex-col items-center justify-center p-8 relative overflow-hidden">
      
      <div class="absolute inset-0 opacity-[0.03] pointer-events-none" style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 32px 32px;"></div>

      <div 
        class="grid gap-1 p-3 bg-zinc-950 border border-zinc-800 rounded-xl shadow-2xl z-10"
        style="grid-template-columns: repeat({larghezza}, minmax(0, 1fr));">
        
        {#each mappa as tipoCella, indice}
        
        <div 
            onclick={() => coloraCella(indice)}
            oncontextmenu={(e) => cancellaCella(e, indice)}
            onmouseenter={(e) => { 
                if (e.buttons === 1) coloraCella(indice); 
                if (e.buttons === 2) cancellaCella(e, indice); 
            }}
            class="w-10 h-10 md:w-12 md:h-12 border border-zinc-800/80 rounded-md cursor-crosshair transition-all duration-100 flex items-center justify-center text-xl select-none hover:brightness-150 hover:scale-105 active:scale-95 {strumenti[tipoCella].color}">
            
            {#if strumenti[tipoCella].img}
                <img src={strumenti[tipoCella].img} draggable="false" class="w-full h-full object-cover [image-rendering:pixelated]" alt={tipoCella} />
            {:else}
                {strumenti[tipoCella].icon}
            {/if}
        </div>
      {/each}
        
      </div>
      
      <div class="mt-6 text-zinc-600 font-mono text-xs font-bold tracking-widest uppercase">
        {larghezza}x{altezza} Units // {totaleCelle} Celle Totali
      </div>
    </section>

  </main>
</div>