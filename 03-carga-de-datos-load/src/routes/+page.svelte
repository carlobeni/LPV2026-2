<script>
  // En Svelte 5 se desestructura 'data' proveniente de +page.server.js con $props()
  let { data } = $props();

  // Runes reactivas de cálculo derivado
  let totalCriticos = $derived(
    data.sensores.filter(s => s.estado === 'ADVERTENCIA' || s.estado === 'CRITICO').length
  );
</script>

<svelte:head>
  <title>03. Carga de Datos en Servidor (load)</title>
</svelte:head>

<div class="contenedor">
  <header class="header">
    <span class="badge">SvelteKit +page.server.js</span>
    <h1>Red de Telemetría Industrial</h1>
    <p class="sub">
      Datos cargados en el servidor a las <strong>{data.timestampServidor}</strong> 
      ({data.sensores.length} de {data.totalDispositivos} nodos visualizados).
    </p>
  </header>

  <!-- Filtros rápidos vía URL -->
  <div class="barra-filtros">
    <span>Filtrar por tipo:</span>
    <a href="?" class:activo={data.filtroActivo === 'todos'}>Todos</a>
    <a href="?tipo=temperatura" class:activo={data.filtroActivo === 'temperatura'}>Temperatura</a>
    <a href="?tipo=presion" class:activo={data.filtroActivo === 'presion'}>Presión</a>
    <a href="?tipo=flujo" class:activo={data.filtroActivo === 'flujo'}>Flujo</a>
    <a href="?tipo=vibracion" class:activo={data.filtroActivo === 'vibracion'}>Vibración</a>
  </div>

  {#if totalCriticos > 0}
    <div class="alerta-banner">
      ⚠️ Se detectaron {totalCriticos} sensores en estado de ADVERTENCIA o CRÍTICO.
    </div>
  {/if}

  <div class="grid-sensores">
    {#each data.sensores as sensor (sensor.id)}
      <div class="sensor-tarjeta">
        <div class="sensor-top">
          <span class="tipo-tag">{sensor.tipo}</span>
          <span class="estado-tag" class:alerta={sensor.estado === 'ADVERTENCIA'}>
            {sensor.estado}
          </span>
        </div>

        <h3>{sensor.tag}</h3>

        <div class="valor-caja">
          <span class="num">{sensor.valor}</span>
          <span class="uni">{sensor.unidad}</span>
        </div>

        <a href="/sensores/{sensor.id}" class="btn-detalle">
          Ver Ficha Técnica &rarr;
        </a>
      </div>
    {:else}
      <p class="vacio">No hay sensores disponibles para el filtro seleccionado.</p>
    {/each}
  </div>

  <div class="caja-prueba-error">
    <h4>Probar Manejo de Errores con <code>error(404)</code>:</h4>
    <p>Haz clic en este enlace para solicitar un sensor inexistente y observar la captura en <code>+error.svelte</code>:</p>
    <a href="/sensores/sensor-inexistente-99" class="btn-error">
      Solicitar Sensor Inexistente (Error 404) &rarr;
    </a>
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
    max-width: 950px;
    margin: 2.5rem auto;
    padding: 0 1.5rem;
  }

  .badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: #58a6ff;
    background: rgba(88, 166, 255, 0.12);
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
    margin: 0 0 1.75rem 0;
  }

  .barra-filtros {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: #161b22;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    border: 1px solid #30363d;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    font-size: 0.85rem;
  }

  .barra-filtros span {
    color: #8b949e;
  }

  .barra-filtros a {
    color: #c9d1d9;
    text-decoration: none;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    transition: background 0.2s;
  }

  .barra-filtros a:hover {
    background: #21262d;
  }

  .barra-filtros a.activo {
    background: #1f6feb;
    color: #ffffff;
    font-weight: 600;
  }

  .alerta-banner {
    background: rgba(210, 153, 34, 0.15);
    border: 1px solid #d29922;
    color: #e3b341;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
  }

  .grid-sensores {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.25rem;
    margin-bottom: 2.5rem;
  }

  .sensor-tarjeta {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .sensor-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.75rem;
  }

  .tipo-tag {
    font-size: 0.7rem;
    text-transform: uppercase;
    color: #8b949e;
    font-weight: 600;
  }

  .estado-tag {
    font-size: 0.7rem;
    font-weight: 700;
    color: #3fb950;
    background: rgba(63, 185, 80, 0.1);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
  }

  .estado-tag.alerta {
    color: #d29922;
    background: rgba(210, 153, 34, 0.1);
  }

  h3 {
    margin: 0 0 1rem 0;
    font-size: 1.05rem;
    color: #ffffff;
  }

  .valor-caja {
    background: #0d1117;
    border-radius: 6px;
    padding: 0.75rem;
    text-align: center;
    margin-bottom: 1.25rem;
  }

  .num {
    font-size: 1.8rem;
    font-weight: 700;
    color: #58a6ff;
    font-family: ui-monospace, monospace;
  }

  .uni {
    font-size: 0.9rem;
    color: #8b949e;
    margin-left: 0.25rem;
  }

  .btn-detalle {
    display: block;
    background: #21262d;
    border: 1px solid #30363d;
    color: #e6edf3;
    text-align: center;
    text-decoration: none;
    padding: 0.5rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
  }

  .btn-detalle:hover {
    background: #30363d;
    border-color: #58a6ff;
  }

  .caja-prueba-error {
    background: #161b22;
    border: 1px dashed #484f58;
    border-radius: 8px;
    padding: 1.5rem;
  }

  .caja-prueba-error h4 {
    margin: 0 0 0.5rem 0;
    color: #f85149;
  }

  .caja-prueba-error p {
    color: #8b949e;
    font-size: 0.9rem;
    margin: 0 0 1rem 0;
  }

  .btn-error {
    display: inline-block;
    background: rgba(248, 81, 73, 0.15);
    border: 1px solid rgba(248, 81, 73, 0.4);
    color: #ff7b72;
    text-decoration: none;
    padding: 0.5rem 0.85rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
  }

  .btn-error:hover {
    background: rgba(248, 81, 73, 0.25);
  }
</style>
