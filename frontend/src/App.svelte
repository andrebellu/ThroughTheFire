<script>
  // 1. LA MENTE (Dati e Variabili)
  // Creiamo delle variabili base per la nostra mappa
  let larghezza = 5;
  let altezza = 5;
  
  // Questa variabile ricorda cosa vogliamo disegnare
  let strumentoAttivo = "Muro"; 
</script>

<main>
  <h1>Editor Mappa - Through The Fire</h1>

  <div class="pannello">
    <h2>Impostazioni</h2>
    <label>Larghezza griglia: 
      <input type="number" bind:value={larghezza} min="3" max="20">
    </label>
    
    <label>Altezza griglia: 
      <input type="number" bind:value={altezza} min="3" max="20">
    </label>

    <p>La tua mappa sarà grande: <strong>{larghezza} x {altezza}</strong> celle.</p>
  </div>

  <div class="pannello">
    <h2>Strumenti</h2>
    <p>Strumento selezionato: <strong>{strumentoAttivo}</strong></p>
    
    <button on:click={() => strumentoAttivo = 'Muro'}>🧱 Disegna Muro</button>
    <button on:click={() => strumentoAttivo = 'Fuoco'}>🔥 Disegna Fuoco</button>
    <button on:click={() => strumentoAttivo = 'Robot'}>🤖 Piazza Robot</button>
    <button on:click={() => strumentoAttivo = 'Civile'}>🧑 Piazza Civile</button>
  </div>
</main>

<style>
  /* 3. IL VESTITO (Estetica) */
  main {
    font-family: Arial, sans-serif;
    padding: 20px;
    max-width: 600px;
    margin: 0 auto; /* Centra tutto nello schermo */
  }

  .pannello {
    background-color: #f4f4f9;
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 8px;
    border: 1px solid #ddd;
  }

  button {
    background-color: #2c3e50;
    color: white;
    border: none;
    padding: 10px 15px;
    margin-right: 5px;
    border-radius: 4px;
    cursor: pointer;
  }

  button:hover {
    background-color: #1a252f;
  }

  input {
    width: 50px;
    margin-right: 20px;
  }
</style>