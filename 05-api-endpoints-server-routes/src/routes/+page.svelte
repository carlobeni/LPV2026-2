<script>
  // Estados reactivos con Runes de Svelte 5
  let sensores = $state([]);
  let cargando = $state(false);
  let filtroBusqueda = $state('');

  // Estados para telemetría SSE
  let streamConectado = $state(false);
  let ultimaLectura = $state(null);
  let historialStream = $state([]);

  // Consumo tradicional con fetch()
  async function cargarSensores() {
    cargando = true;
    try {
      const url = filtroBusqueda 
        ? `/api/sensores?q=${encodeURIComponent(filtroBusqueda)}` 
        : '/api/sensores';
      const res = await fetch(url);
      const data = await res.json();
      sensores = data.sensores || [];
    } catch (err) {
      console.error('Fallo al consultar API REST:', err);
    } finally {
      cargando = false;
    }
  }

  // Conexión dinámica a Server-Sent Events (SSE)
  let eventSource = null;
  function toggleStream() {
    if (streamConectado) {
      if (eventSource) {
        eventSource.close();
        eventSource = null;
      }
      streamConectado = false;
    } else {
      eventSource = new EventSource('/api/telemetria/stream');
      streamConectado = true;

      eventSource.onmessage = (e) => {
        const payload = JSON.parse(e.data);
        ultimaLectura = payload;
        historialStream = [...historialStream.slice(-9), payload];
      };

      eventSource.onerror = () => {
        streamConectado = false;
        if (eventSource) eventSource.close();
      };
    }
  }

  // Cargar lista inicial
  $effect(() => {
    cargarSensores();
    return () => {
      if (eventSource) eventSource.close();
    };
  });
</script>

<svelte:head>
  <title>05. Endpoints de API REST y Streaming SSE</title>
</svelte:head>

<div class="contenedor">
  <header class="header">
    <span class="badge">SvelteKit +server.js</span>
    <h1>Endpoints de API REST y Streaming en Tiempo Real</h1>
    <p class="sub">Consumo de APIs declaradas en rutas de servidor y recepción de telemetría continua</p>
  </header>

  <div class="paneles-grid">
    <!-- Panel Izquierdo: API REST y Exportación -->
    <div class="tarjeta-panel">
      <div class="panel-header">
        <h3>Cliente API REST (/api/sensores)</h3>
        <a href="/api/exportar/csv" class="btn-descarga">
          📥 Descargar CSV
        </a>
      </div>

      <div class="barra-busqueda">
        <input 
          type="text" 
          bind:value={filtroBusqueda} 
          placeholder="Filtrar por tag (ej. PT100)..." 
          onkeydown={(e) => e.key === 'Enter' && cargarSensores()}
        />
        <button onclick={cargarSensores} class="btn-buscar" disabled={cargando}>
          {cargando ? 'Consultando...' : 'Consultar'}
        </button>
      </div>

      <div class="tabla-respuestas">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Tag</th>
              <th>Magnitud</th>
            </tr>
          </thead>
          <tbody>
            {#each sensores as s}
              <tr>
                <td><code>{s.id}</code></td>
                <td><strong>{s.tag}</strong></td>
                <td>{s.valor} {s.unidad}</td>
              </tr>
            {:else}
              <tr>
                <td colspan="3" class="vacio">No se obtuvieron registros del endpoint.</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Panel Derecho: Streaming Server-Sent Events (SSE) -->
    <div class="tarjeta-panel">
      <div class="panel-header">
        <h3>Streaming SSE en Vivo</h3>
        <button 
          onclick={toggleStream} 
          class="btn-stream" 
          class:conectado={streamConectado}
        >
          {streamConectado ? 'Detener Stream' : 'Iniciar SSE Stream'}
        </button>
      </div>

      {#if ultimaLectura}
        <div class="metricas-en-vivo">
          <div class="metrica-caja">
            <span class="m-label">Temperatura</span>
            <span class="m-val">{ultimaLectura.temperatura} <small>°C</small></span>
          </div>
          <div class="metrica-caja">
            <span class="m-label">Presión</span>
            <span class="m-val">{ultimaLectura.presion} <small>bar</small></span>
          </div>
          <div class="metrica-caja">
            <span class="m-label">Régimen</span>
            <span class="m-val">{ultimaLectura.rpm} <small>RPM</small></span>
          </div>
        </div>

        <div class="historial-scroll">
          <h4>Últimas tramas recibidas:</h4>
          <ul>
            {#each historialStream as h}
              <li>
                <span class="time">[{h.timestamp}]</span>
                <span>T: {h.temperatura}°C | P: {h.presion}bar | RPM: {h.rpm}</span>
              </li>
            {/each}
          </ul>
        </div>
      {:else}
        <div class="placeholder-stream">
          <p>Presiona <strong>"Iniciar SSE Stream"</strong> para comenzar a recibir paquetes en tiempo real desde <code>/api/telemetria/stream</code>.</p>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    background: #0d1117;
    color: #e6edf3;
    font-family: system-ui, sans-serif;
  }

  .contenedor {
    max-width: 1100px;
    margin: 2.5rem auto;
    padding: 0 1.5rem;
  }

  .badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: #3fb950;
    background: rgba(63, 185, 80, 0.12);
    border-radius: 9999px;
    margin-bottom: 0.75rem;
    text-transform: uppercase;
  }

  h1 {
    font-size: 2.1rem;
    margin: 0 0 0.5rem 0;
    color: #ffffff;
  }

  .sub {
    color: #8b949e;
    margin: 0 0 2rem 0;
  }

  .paneles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
    gap: 1.5rem;
  }

  .tarjeta-panel {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.75rem;
    display: flex;
    flex-direction: column;
  }

  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.25rem;
  }

  .panel-header h3 {
    margin: 0;
    font-size: 1.15rem;
    color: #ffffff;
  }

  .btn-descarga {
    background: #21262d;
    border: 1px solid #30363d;
    color: #58a6ff;
    padding: 0.4rem 0.75rem;
    border-radius: 6px;
    text-decoration: none;
    font-size: 0.8rem;
    font-weight: 600;
  }

  .btn-descarga:hover {
    background: #30363d;
  }

  .barra-busqueda {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  input {
    flex: 1;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #e6edf3;
    padding: 0.55rem 0.75rem;
    font-size: 0.9rem;
    outline: none;
  }

  input:focus {
    border-color: #58a6ff;
  }

  .btn-buscar {
    background: #1f6feb;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 0 1rem;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
  }

  .btn-buscar:hover:not(:disabled) {
    background: #388bfd;
  }

  .tabla-respuestas {
    overflow-x: auto;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    text-align: left;
  }

  th, td {
    padding: 0.65rem 0.75rem;
    border-bottom: 1px solid #21262d;
  }

  th {
    color: #8b949e;
    font-weight: 600;
  }

  td code {
    color: #8957e5;
  }

  .vacio {
    text-align: center;
    color: #8b949e;
    padding: 1.5rem;
  }

  .btn-stream {
    background: #238636;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 0.45rem 0.85rem;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
  }

  .btn-stream.conectado {
    background: #da3633;
  }

  .metricas-en-vivo {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.25rem;
  }

  .metrica-caja {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 0.75rem;
    text-align: center;
  }

  .m-label {
    display: block;
    font-size: 0.7rem;
    color: #8b949e;
    text-transform: uppercase;
  }

  .m-val {
    font-size: 1.3rem;
    font-weight: 700;
    color: #58a6ff;
    font-family: ui-monospace, monospace;
  }

  .m-val small {
    font-size: 0.75rem;
    color: #8b949e;
  }

  .historial-scroll {
    background: #0d1117;
    border-radius: 6px;
    padding: 0.75rem;
    flex: 1;
  }

  .historial-scroll h4 {
    margin: 0 0 0.5rem 0;
    font-size: 0.75rem;
    color: #8b949e;
    text-transform: uppercase;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    font-family: ui-monospace, monospace;
    font-size: 0.8rem;
  }

  li {
    color: #c9d1d9;
    display: flex;
    gap: 0.5rem;
  }

  .time {
    color: #8b949e;
  }

  .placeholder-stream {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    text-align: center;
    padding: 2rem;
    color: #8b949e;
    font-size: 0.95rem;
  }
</style>
