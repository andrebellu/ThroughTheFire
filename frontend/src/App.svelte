<script>
  let larghezza = $state(12);
  let altezza   = $state(10);
  let strumentoAttivo = $state('Muro');
  let livelloAttivoId = $state(null);   //traccia il livello caricato

  let mappa = $state(Array(larghezza * altezza).fill('Vuoto'));
  let totaleCelle = $derived(larghezza * altezza);

  $effect(() => {
    const nuovaDimensione = larghezza * altezza;
    if (mappa.length !== nuovaDimensione) {
      mappa = Array(nuovaDimensione).fill('Vuoto');
      livelloAttivoId = null;   
    }
  });


  const strumenti = {
    'Muro':   { img: 'Stone.jpg',       desc: 'Blocca',       color: 'bg-zinc-700',    activeClass: 'ring-zinc-400/30' },
    'Fuoco':  { img: 'FirePixel.png',   desc: 'Pericolo',     color: 'bg-orange-900',  activeClass: 'border-orange-500 ring-orange-500/30' },
    'Robot':  { img: 'Robot.png',       desc: 'Start',        color: 'bg-blue-900',    activeClass: 'border-blue-500 ring-blue-500/30' },
    'Civile': { img: 'CivilPixel.png',  desc: 'Target',       color: 'bg-emerald-900', activeClass: 'border-emerald-500 ring-emerald-500/30' },
    'Arrivo': { icon: '🏁',             desc: 'Finish Point', color: 'bg-emerald-900', activeClass: 'border-emerald-500 ring-emerald-500/30' },
    'Vuoto':  { icon: '',               desc: 'Cella vuota',  color: 'bg-zinc-800/50', activeClass: '' }
  };

  const coloriMinimap = {
    'Muro':   '#3f3f46',
    'Fuoco':  '#f97316',
    'Robot':  '#60a5fa',
    'Civile': '#34d399',
    'Arrivo': '#fbbf24',
    'Vuoto':  '#09090b'
  };


  function schemaToMappa(schema) {
    const charMap = {
      '#': 'Muro', 'R': 'Robot', 'F': 'Fuoco',
      'C': 'Civile', 'A': 'Arrivo', '.': 'Vuoto'
    };
    return schema
      .trim()
      .split('\n')
      .flatMap(riga => riga.split('').map(c => charMap[c] ?? 'Vuoto'));
  }

  const livelliPredefiniti = [
    {
      id: 1,
      nome: 'Easy mode',
      difficolta: 'Facile',
      coloreDiff: '#34d399', 
      larghezza: 12,
      altezza: 10,

      schema:
`############
#R.........#
##########.#
#..........#
#.##########
#....F.....#
##########.#
#..........#
#.##########
#........CA#`
    },
    {
      id: 2,
      difficolta: 'Medio',
      coloreDiff: '#facc15',   // yellow
      larghezza: 12,
      altezza: 10,

      schema:
`############
#R.#.......#
#..#.#####.#
#..#.#...#.#
#..#.#.#.#.#
#....#.#.#.#
##.###.#.#.#
#..#F..#.C.#
#..####.##.#
#......#..A#`
    },
    {
      id: 3,
      difficolta: 'Difficile',
      coloreDiff: '#f87171',   // red
      larghezza: 12,
      altezza: 10,

      schema:
`############
#R.........#
#..FF..FF..#
#..........#
#.FF....FF.#
#..........#
#..FF..FF..#
#..........#
#.FF....FF.#
#.......CA.#`
    }
  ].map(l => ({ ...l, mappaPreview: schemaToMappa(l.schema) }));


  function caricaLivello(livello) {

    larghezza       = livello.larghezza;
    altezza         = livello.altezza;
    mappa           = [...livello.mappaPreview];  
    livelloAttivoId = livello.id;
  }

  function nuovaGriglia() {
    mappa           = Array(larghezza * altezza).fill('Vuoto');
    livelloAttivoId = null;
    status          = '🟢 Griglia pulita';
  }

  function coloraCella(indice) {
    if (strumentoAttivo === 'Robot') {
      const old = mappa.findIndex(c => c === 'Robot');
      if (old !== -1) mappa[old] = 'Vuoto';
    }
    if (strumentoAttivo === 'Arrivo') {
      const old = mappa.findIndex(c => c === 'Arrivo');
      if (old !== -1) mappa[old] = 'Vuoto';
    }
    mappa[indice] = strumentoAttivo;
  }

  function cancellaCella(evento, indice) {
    evento.preventDefault();
    mappa[indice] = 'Vuoto';
  }
</script>


<div class="h-screen w-full bg-zinc-950 text-zinc-100 flex flex-col font-sans selection:bg-orange-500/30">

  <header class="shrink-0 w-full py-6 flex flex-col items-center justify-center">
    <h1 class="text-orange-500 font-black text-4xl tracking-tighter uppercase italic leading-none drop-shadow-[0_0_15px_rgba(249,115,22,0.4)]">
      THROUGH THE FIRE
    </h1>
  </header>

  <main class="flex-1 flex px-6 pb-6 gap-6 overflow-hidden">

    <!-- ─── SIDEBAR ──────────────────────────────────────────── -->
    <aside class="w-80 shrink-0 h-full overflow-y-auto flex flex-col gap-6 bg-zinc-900/80 backdrop-blur-xl p-6 rounded-2xl border border-zinc-800 shadow-2xl">

      <!-- Dimensioni griglia -->
      <section class="space-y-3">
        <h2 class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest">Dimensioni Griglia</h2>
        <div class="flex gap-3">
          <label class="flex-1 bg-zinc-950 p-3 rounded-xl border border-zinc-800 focus-within:border-orange-500/50 transition-colors">
            <span class="block text-[10px] text-zinc-500 uppercase font-bold mb-1">Larghezza</span>
            <input type="number" min="5" max="30" bind:value={larghezza}
              class="w-full bg-transparent text-orange-400 font-mono text-xl font-bold outline-none" />
          </label>
          <label class="flex-1 bg-zinc-950 p-3 rounded-xl border border-zinc-800 focus-within:border-orange-500/50 transition-colors">
            <span class="block text-[10px] text-zinc-500 uppercase font-bold mb-1">Altezza</span>
            <input type="number" min="5" max="30" bind:value={altezza}
              class="w-full bg-transparent text-orange-400 font-mono text-xl font-bold outline-none" />
          </label>
        </div>
      </section>

      <div class="h-px bg-zinc-800"></div>

      <!-- ── LIVELLI PREDEFINITI ────────────────────────────── -->
      <section class="space-y-3">
        <div class="flex items-center justify-between">
          <h2 class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest">Livelli Predefiniti</h2>
          <!-- Pulsante "Nuovo" resetta la griglia alle dimensioni correnti -->
          <button
            onclick={nuovaGriglia}
            class="text-[10px] text-zinc-500 hover:text-zinc-200 transition-colors uppercase tracking-widest font-bold px-2 py-1 rounded-md hover:bg-zinc-800 border border-transparent hover:border-zinc-700">
            + Nuovo
          </button>
        </div>

        <div class="space-y-2">
          {#each livelliPredefiniti as livello}
            <button
              onclick={() => caricaLivello(livello)}
              class="w-full flex items-center gap-3 p-3 rounded-xl border-2 transition-all duration-200 text-left
              {livelloAttivoId === livello.id
                ? 'bg-zinc-800 border-orange-500/40 ring-1 ring-orange-500/20 shadow-lg shadow-orange-900/20'
                : 'border-zinc-800/50 bg-zinc-950 hover:bg-zinc-900 hover:border-zinc-700'}">

             
              <div
                class="shrink-0 rounded-sm overflow-hidden border border-zinc-800/80"
                style="display:grid;
                       grid-template-columns: repeat({livello.larghezza}, 3px);
                       gap: 0.5px;
                       padding: 1px;
                       background: #18181b;">
                {#each livello.mappaPreview as cella}
                  <div style="width:3px; height:3px; background:{coloriMinimap[cella] ?? coloriMinimap.Vuoto};"></div>
                {/each}
              </div>

           
              <div class="flex-1 min-w-0">
                <div class="text-xs font-bold text-zinc-200 truncate">{livello.nome}</div>
                <div class="flex items-center gap-1.5 mt-0.5">
                  <span class="text-[10px] font-bold uppercase tracking-widest" style="color:{livello.coloreDiff}">
                    {livello.difficolta}
                  </span>
                  <span class="text-zinc-700">·</span>
                  <span class="text-[10px] font-mono text-zinc-600">{livello.larghezza}×{livello.altezza}</span>
                </div>
              </div>

            
              {#if livelloAttivoId === livello.id}
                <span class="text-orange-400 text-xs shrink-0">✓</span>
              {:else}
                <span class="text-zinc-700 text-xs shrink-0">→</span>
              {/if}
            </button>
          {/each}
        </div>
      </section>

      <div class="h-px bg-zinc-800"></div>

  
      <section class="flex-1">
        <h2 class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest mb-4">
          Seleziona gli strumenti per personalizzare lo scenario
        </h2>
        <div class="grid grid-cols-2 gap-3">
          {#each Object.entries(strumenti) as [id, data]}
            {#if id !== 'Vuoto'}
              <button
                onclick={() => strumentoAttivo = id}
                class="flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-all duration-200
                {strumentoAttivo === id
                  ? `bg-zinc-800 ${data.activeClass} ring-4 shadow-lg scale-105`
                  : 'border-zinc-800/50 bg-zinc-950 hover:bg-zinc-900'}">
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

      <!-- Azioni -->
      <div class="mt-auto pt-2 space-y-3">
        <button class="w-full py-4 rounded-xl bg-orange-600 hover:bg-orange-500 text-white font-black tracking-widest uppercase shadow-[0_0_20px_rgba(234,88,12,0.3)] transition-all active:scale-95">
          Salva in Database
        </button>
        <p class="text-center text-[10px] font-mono text-zinc-600 uppercase tracking-widest">{status}</p>
      </div>
    </aside>

    <!-- ─── GRIGLIA ───────────────────────────────────────────── -->
    <section class="flex-1 h-full bg-zinc-900/30 rounded-2xl border border-zinc-800/50 flex flex-col items-center justify-center p-8 relative overflow-hidden">

      <!-- Sfondo punteggiato decorativo -->
      <div class="absolute inset-0 opacity-[0.03] pointer-events-none"
           style="background-image: radial-gradient(circle at 2px 2px, white 1px, transparent 0); background-size: 32px 32px;"></div>

      <!-- Griglia principale -->
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
              <img src={strumenti[tipoCella].img} draggable="false"
                class="w-full h-full object-cover [image-rendering:pixelated]" alt={tipoCella} />
            {:else}
              {strumenti[tipoCella].icon}
            {/if}
          </div>
        {/each}
      </div>

      <!-- Info dimensioni -->
      <div class="mt-6 text-zinc-600 font-mono text-xs font-bold tracking-widest uppercase">
        {larghezza}×{altezza} Units // {totaleCelle} Celle Totali
      </div>
    </section>

  </main>
</div>