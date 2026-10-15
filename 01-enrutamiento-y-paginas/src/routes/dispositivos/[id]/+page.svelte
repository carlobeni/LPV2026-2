<script>
  import { page } from '$app/state';

  // En Svelte 5 leemos el parámetro usando reactividad derivada
  let id = $derived(page.params.id);

  // Simulación de metadatos según el ID ingresado
  let esSensorTemperatura = $derived(id.toUpperCase().includes('TEMP') || id.toUpperCase().includes('PT'));
  let esMotor = $derived(id.toUpperCase().includes('MOTOR') || id.toUpperCase().includes('NEMA'));
</script>

<svelte:head>
  <title>Dispositivo: {id} — Telemetría</title>
</svelte:head>

<div class="contenedor">
  <div class="tarjeta-nodo">
    <a href="/" class="volver">&larr; Volver al menú principal</a>

    <header class="nodo-header">
      <div class="tipo-badge">
        {#if esSensorTemperatura}
          🌡️ Sensor Térmico
        {:else if esMotor}
          ⚙️ Actuador / Motor
        {:else}
          📡 Nodo Genérico
        {/if}
      </div>
      <h1>Dispositivo: <span class="destacado">{id}</span></h1>
      <p class="ruta-info">Ruta capturada dinámicamente desde: <code>src/routes/dispositivos/[id]/+page.svelte</code></p>
    </header>

    <div class="parametros-inspeccion">
      <h3>Inspección del Objeto <code>page.params</code>:</h3>
      <pre><code>{JSON.stringify({ id: id }, null, 2)}</code></pre>
    </div>

    <div class="panel-ejemplo">
      <h4>Estado Operativo del Canal:</h4>
      <div class="metricas-grid">
        <div class="metrica">
          <span class="label">Tag de Canal</span>
          <span class="valor">{id}</span>
        </div>
        <div class="metrica">
          <span class="label">Estado Bus</span>
          <span class="valor online">ONLINE (CAN 2.0B)</span>
        </div>
        <div class="metrica">
          <span class="label">Frecuencia de Muestreo</span>
          <span class="valor">100 Hz</span>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .contenedor {
    max-width: 800px;
    margin: 3rem auto;
    padding: 1.5rem;
  }

  .tarjeta-nodo {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 2rem;
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

  .nodo-header {
    border-bottom: 1px solid #30363d;
    padding-bottom: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .tipo-badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    font-size: 0.8rem;
    font-weight: 600;
    background: #1f6feb;
    color: #ffffff;
    border-radius: 9999px;
    margin-bottom: 0.75rem;
  }

  h1 {
    font-size: 1.8rem;
    margin: 0 0 0.5rem 0;
    color: #ffffff;
  }

  .destacado {
    color: #58a6ff;
    font-family: ui-monospace, monospace;
  }

  .ruta-info {
    color: #8b949e;
    margin: 0;
    font-size: 0.9rem;
  }

  code {
    background: #0d1117;
    color: #f0883e;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-family: ui-monospace, monospace;
    font-size: 0.85em;
  }

  .parametros-inspeccion {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
  }

  .parametros-inspeccion h3 {
    margin: 0 0 0.5rem 0;
    font-size: 0.95rem;
    color: #e6edf3;
  }

  pre {
    margin: 0;
  }

  pre code {
    background: transparent;
    color: #7ee787;
    padding: 0;
    font-size: 0.9rem;
  }

  .panel-ejemplo {
    background: #21262d;
    border-radius: 8px;
    padding: 1.25rem;
  }

  .panel-ejemplo h4 {
    margin: 0 0 1rem 0;
    font-size: 0.95rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .metricas-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
  }

  .metrica {
    background: #161b22;
    padding: 0.75rem 1rem;
    border-radius: 6px;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .metrica .label {
    font-size: 0.75rem;
    color: #8b949e;
  }

  .metrica .valor {
    font-size: 1rem;
    font-weight: 600;
    color: #ffffff;
    font-family: ui-monospace, monospace;
  }

  .metrica .valor.online {
    color: #3fb950;
  }
</style>
