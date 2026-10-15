<script>
  let { data } = $props();
  let s = $derived(data.sensor);
</script>

<svelte:head>
  <title>Ficha Técnica: {s.tag}</title>
</svelte:head>

<div class="contenedor">
  <div class="ficha-sensor">
    <a href="/" class="volver">&larr; Volver al listado</a>

    <header class="ficha-header">
      <span class="tag-id">{s.id}</span>
      <h1>{s.tag}</h1>
      <p class="tipo">{s.tipo}</p>
    </header>

    <div class="specs-grid">
      <div class="spec">
        <span class="label">Rango Operativo</span>
        <span class="val">{s.rango}</span>
      </div>
      <div class="spec">
        <span class="label">Precisión</span>
        <span class="val">{s.precision}</span>
      </div>
      <div class="spec">
        <span class="label">Protocolo de Bus</span>
        <span class="val">{s.bus}</span>
      </div>
      <div class="spec">
        <span class="label">Dirección / Canal</span>
        <span class="val">{s.direccion}</span>
      </div>
    </div>

    <div class="seccion-muestras">
      <h3>Últimas 4 Lecturas Registradas:</h3>
      <div class="muestras-fila">
        {#each s.historialMuestras as m, idx}
          <div class="muestra-chip">
            <span class="muestra-index">T-{4 - idx}</span>
            <span class="muestra-val">{m}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>
</div>

<style>
  .contenedor {
    max-width: 750px;
    margin: 3rem auto;
    padding: 0 1.5rem;
  }

  .ficha-sensor {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 2.25rem;
  }

  .volver {
    display: inline-block;
    color: #58a6ff;
    text-decoration: none;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
  }

  .volver:hover {
    text-decoration: underline;
  }

  .tag-id {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    color: #8957e5;
    background: rgba(137, 87, 229, 0.15);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    margin-bottom: 0.5rem;
  }

  h1 {
    font-size: 1.8rem;
    margin: 0 0 0.35rem 0;
    color: #ffffff;
  }

  .tipo {
    color: #8b949e;
    margin: 0 0 1.75rem 0;
    font-size: 0.95rem;
  }

  .specs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .spec {
    background: #0d1117;
    border: 1px solid #21262d;
    padding: 1rem;
    border-radius: 6px;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  .spec .label {
    font-size: 0.75rem;
    color: #8b949e;
    text-transform: uppercase;
  }

  .spec .val {
    font-size: 0.95rem;
    font-weight: 600;
    color: #e6edf3;
  }

  .seccion-muestras h3 {
    margin: 0 0 0.75rem 0;
    font-size: 1rem;
    color: #ffffff;
  }

  .muestras-fila {
    display: flex;
    gap: 0.75rem;
  }

  .muestra-chip {
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 0.5rem 0.85rem;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .muestra-index {
    font-size: 0.7rem;
    color: #8b949e;
  }

  .muestra-val {
    font-size: 1.1rem;
    font-weight: 700;
    color: #58a6ff;
    font-family: ui-monospace, monospace;
  }
</style>
