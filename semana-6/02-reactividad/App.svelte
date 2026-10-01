<script>
  // ── ESTADO REACTIVO ───────────────────────────────────────────────────────
  // $state() es la "rune" de Svelte 5 para estado reactivo.
  // Cuando cambia, el DOM se actualiza automáticamente.

  let contador = $state(0);
  let paso = $state(1);

  // ── ESTADO DERIVADO ───────────────────────────────────────────────────────
  // $derived() recalcula el valor cada vez que sus dependencias cambian.
  // Similar a una "propiedad computada" en Vue.

  let esPositivo = $derived(contador > 0);
  let esPar = $derived(contador % 2 === 0);
  let cuadrado = $derived(contador ** 2);
  let etiquetaParidad = $derived(esPar ? "Par ✓" : "Impar ✗");

  // ── HISTORIAL ────────────────────────────────────────────────────────────
  let historial = $state([]);

  // ── EFECTO ───────────────────────────────────────────────────────────────
  // $effect() se ejecuta cada vez que el estado del que depende cambia.
  $effect(() => {
    // Registramos en el historial (máximo 8 entradas)
    historial = [contador, ...historial].slice(0, 8);
  });

  // ── FUNCIONES ─────────────────────────────────────────────────────────────
  function incrementar() {
    contador += paso;
  }

  function decrementar() {
    contador -= paso;
  }

  function reiniciar() {
    contador = 0;
    historial = [];
  }
</script>

<!-- ── TEMPLATE ──────────────────────────────────────────────────────────── -->
<main>
  <header>
    <h1>⚡ Contador Reactivo</h1>
    <p class="subtitulo">Sección 02 — Estado con <code>$state</code> y <code>$derived</code></p>
  </header>

  <!-- Pantalla del contador -->
  <div class="pantalla" class:positivo={esPositivo} class:negativo={!esPositivo && contador !== 0}>
    <span class="numero">{contador}</span>
    <span class="paridad">{etiquetaParidad}</span>
  </div>

  <!-- Paso -->
  <div class="paso-control">
    <label for="paso">Paso de incremento:</label>
    <input id="paso" type="range" min="1" max="10" bind:value={paso} />
    <span class="paso-valor">{paso}</span>
  </div>

  <!-- Botones de control -->
  <div class="botones">
    <button class="btn btn-dec" onclick={decrementar}>− {paso}</button>
    <button class="btn btn-reset" onclick={reiniciar}>↺ Reset</button>
    <button class="btn btn-inc" onclick={incrementar}>+ {paso}</button>
  </div>

  <!-- Valores derivados -->
  <section class="derivados">
    <h2>Valores <code>$derived</code></h2>
    <div class="grid-derivados">
      <div class="dato">
        <span class="dato-label">Cuadrado</span>
        <span class="dato-valor">{cuadrado}</span>
      </div>
      <div class="dato">
        <span class="dato-label">Es positivo</span>
        <span class="dato-valor">{esPositivo ? "Sí ✅" : "No ❌"}</span>
      </div>
      <div class="dato">
        <span class="dato-label">Paridad</span>
        <span class="dato-valor">{etiquetaParidad}</span>
      </div>
    </div>
  </section>

  <!-- Historial -->
  <section class="historial">
    <h2>Historial (<code>$effect</code>)</h2>
    <div class="chips">
      {#each historial as valor, i}
        <span class="chip" style="opacity: {1 - i * 0.1};">{valor}</span>
      {/each}
      {#if historial.length === 0}
        <span class="vacio">Sin historial aún...</span>
      {/if}
    </div>
  </section>
</main>

<!-- ── ESTILOS ────────────────────────────────────────────────────────────── -->
<style>
  :global(body) {
    margin: 0;
    background: #0f0f1a;
    color: #e2e8f0;
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 2rem 1rem;
  }

  main {
    width: 100%;
    max-width: 480px;
  }

  header {
    text-align: center;
    margin-bottom: 2rem;
  }

  h1 {
    font-size: 2rem;
    margin: 0 0 0.25rem;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .subtitulo {
    color: #64748b;
    font-size: 0.9rem;
    margin: 0;
  }

  /* Pantalla del contador */
  .pantalla {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #1e1b4b;
    border: 2px solid #312e81;
    border-radius: 1.5rem;
    padding: 2rem;
    margin: 0 auto 1.5rem;
    transition: border-color 0.3s, background 0.3s;
  }

  .pantalla.positivo {
    border-color: #4ade80;
    background: #052e16;
  }

  .pantalla.negativo {
    border-color: #f87171;
    background: #2d0a0a;
  }

  .numero {
    font-size: 5rem;
    font-weight: 900;
    line-height: 1;
    font-variant-numeric: tabular-nums;
  }

  .paridad {
    font-size: 1rem;
    color: #94a3b8;
    margin-top: 0.5rem;
  }

  /* Paso */
  .paso-control {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
    background: #1e293b;
    padding: 0.75rem 1rem;
    border-radius: 0.75rem;
  }

  .paso-control label {
    font-size: 0.85rem;
    color: #94a3b8;
    white-space: nowrap;
  }

  .paso-control input[type="range"] {
    flex: 1;
    accent-color: #818cf8;
  }

  .paso-valor {
    font-weight: 700;
    color: #818cf8;
    min-width: 1.5rem;
    text-align: right;
  }

  /* Botones */
  .botones {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
  }

  .btn {
    flex: 1;
    padding: 0.85rem;
    border: none;
    border-radius: 0.75rem;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.1s, opacity 0.2s;
  }

  .btn:active { transform: scale(0.96); }

  .btn-inc { background: #4ade80; color: #052e16; }
  .btn-dec { background: #f87171; color: #450a0a; }
  .btn-reset { background: #334155; color: #e2e8f0; flex: 0.6; }

  /* Derivados */
  .derivados, .historial {
    background: #1e293b;
    border-radius: 1rem;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
  }

  h2 {
    font-size: 0.9rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 0.75rem;
  }

  .grid-derivados {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
  }

  .dato {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #0f172a;
    padding: 0.75rem 0.5rem;
    border-radius: 0.5rem;
  }

  .dato-label { font-size: 0.7rem; color: #64748b; margin-bottom: 0.25rem; }
  .dato-valor { font-size: 0.95rem; font-weight: 700; color: #e2e8f0; }

  /* Historial */
  .chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .chip {
    background: #312e81;
    color: #a5b4fc;
    font-size: 0.85rem;
    font-weight: 700;
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
    font-variant-numeric: tabular-nums;
  }

  .vacio {
    color: #475569;
    font-size: 0.85rem;
    font-style: italic;
  }
</style>
