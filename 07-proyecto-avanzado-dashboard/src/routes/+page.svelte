<script>
  import { enhance } from '$app/forms';

  let { data, form } = $props();

  // Búfer reactivo de telemetría en vivo (Svelte 5 Runes)
  let historialTelemetria = $state([
    { temperatura: 82.1, presion: 4.82, rpm: 1740, vibracion: 1.12, potenciaKW: 93.5, timestamp: '18:00:01' },
    { temperatura: 82.4, presion: 4.85, rpm: 1745, vibracion: 1.14, potenciaKW: 93.8, timestamp: '18:00:02' },
    { temperatura: 82.8, presion: 4.90, rpm: 1752, vibracion: 1.13, potenciaKW: 94.2, timestamp: '18:00:03' },
    { temperatura: 83.2, presion: 4.88, rpm: 1748, vibracion: 1.15, potenciaKW: 94.0, timestamp: '18:00:04' },
    { temperatura: 83.5, presion: 4.92, rpm: 1755, vibracion: 1.16, potenciaKW: 94.5, timestamp: '18:00:05' }
  ]);

  let datoActual = $derived(
    historialTelemetria[historialTelemetria.length - 1] || {
      temperatura: 80.0,
      presion: 5.0,
      rpm: 1750,
      vibracion: 1.15,
      potenciaKW: 90.0,
      timestamp: '--:--:--'
    }
  );

  // Cálculos reactivos con $derived
  let tempPromedio = $derived(
    (historialTelemetria.reduce((acc, d) => acc + d.temperatura, 0) / historialTelemetria.length).toFixed(1)
  );

  let tempMax = $derived(
    Math.max(...historialTelemetria.map(d => d.temperatura)).toFixed(1)
  );

  let errorPresion = $derived(
    (datoActual.presion - data.planta.setpointPresion).toFixed(2)
  );

  // Generador de coordenadas SVG para el gráfico de ondas temporales en tiempo real
  let svgPuntosTemp = $derived.by(() => {
    const ancho = 560;
    const alto = 180;
    const n = historialTelemetria.length;
    if (n < 2) return '';

    return historialTelemetria.map((d, i) => {
      const x = (i / (n - 1)) * ancho;
      // Mapeo de temperatura de 50°C (alto) a 110°C (0)
      const y = alto - ((d.temperatura - 50) / 60) * alto;
      return `${x.toFixed(1)},${Math.max(5, Math.min(alto - 5, y)).toFixed(1)}`;
    }).join(' ');
  });

  let svgPuntosPresion = $derived.by(() => {
    const ancho = 560;
    const alto = 180;
    const n = historialTelemetria.length;
    if (n < 2) return '';

    return historialTelemetria.map((d, i) => {
      const x = (i / (n - 1)) * ancho;
      // Mapeo de presión de 1 bar (alto) a 9 bar (0)
      const y = alto - ((d.presion - 1) / 8) * alto;
      return `${x.toFixed(1)},${Math.max(5, Math.min(alto - 5, y)).toFixed(1)}`;
    }).join(' ');
  });

  // Conexión reactiva a SSE en tiempo real
  let sseConectado = $state(false);
  let ajustandoSetpoint = $state(false);

  $effect(() => {
    const es = new EventSource('/api/telemetria/stream');
    sseConectado = true;

    es.onmessage = (event) => {
      try {
        const muestra = JSON.parse(event.data);
        // Mantener últimos 25 puntos en el osciloscopio
        historialTelemetria = [...historialTelemetria.slice(-24), muestra];
      } catch (err) {
        console.error('Error parseando SSE:', err);
      }
    };

    es.onerror = () => {
      sseConectado = false;
    };

    return () => {
      es.close();
      sseConectado = false;
    };
  });
</script>

<svelte:head>
  <title>SCADA Telemetría — Dashboard Avanzado SvelteKit</title>
</svelte:head>

<div class="dashboard-grid">
  <!-- COLUMNA PRINCIPAL (TELEMETRÍA Y GRÁFICOS) -->
  <div class="col-telemetria">
    <!-- Banner de Parada de Emergencia -->
    {#if data.planta.paradaEmergenciaActiva}
      <div class="banner-critico">
        <div class="critico-contenido">
          <span class="alerta-icono">🚨</span>
          <div>
            <h3>PARADA DE EMERGENCIA EN PLANTA ACTIVA</h3>
            <p>Todos los actuadores primarios han sido desacoplados por el enclavamiento de seguridad.</p>
          </div>
        </div>
        <form method="POST" action="?/rearmarSistema" use:enhance>
          <button type="submit" class="btn-rearmar">REARMAR PLANTA</button>
        </form>
      </div>
    {/if}

    <!-- Alertas de Formulario -->
    {#if form?.error}
      <div class="banner-feedback error">❌ {form.error}</div>
    {/if}
    {#if form?.mensaje}
      <div class="banner-feedback exito">✅ {form.mensaje}</div>
    {/if}

    <!-- KPI Cards (Métricas Físicas) -->
    <div class="kpi-cards">
      <!-- KPI 1: Temperatura -->
      <div class="kpi-card" class:alerta={datoActual.temperatura > 95}>
        <div class="kpi-top">
          <span class="kpi-label">TEMPERATURA COLECTOR</span>
          <span class="kpi-badge">RTD PT-100</span>
        </div>
        <div class="kpi-valor">
          {datoActual.temperatura} <small>°C</small>
        </div>
        <div class="kpi-stats">
          <span>Media: <strong>{tempPromedio} °C</strong></span>
          <span>Pico: <strong>{tempMax} °C</strong></span>
        </div>
      </div>

      <!-- KPI 2: Presión -->
      <div class="kpi-card" class:alerta={datoActual.presion > 6.5}>
        <div class="kpi-top">
          <span class="kpi-label">PRESIÓN EN COLECTOR</span>
          <span class="kpi-badge">4-20 mA</span>
        </div>
        <div class="kpi-valor">
          {datoActual.presion} <small>bar</small>
        </div>
        <div class="kpi-stats">
          <span>Consigna: <strong>{data.planta.setpointPresion} bar</strong></span>
          <span>Error (e): <strong class:positivo={Number(errorPresion) >= 0}>{errorPresion} bar</strong></span>
        </div>
      </div>

      <!-- KPI 3: Régimen Turbina -->
      <div class="kpi-card">
        <div class="kpi-top">
          <span class="kpi-label">VELOCIDAD ROTACIONAL</span>
          <span class="kpi-badge">ENCODER</span>
        </div>
        <div class="kpi-valor">
          {datoActual.rpm} <small>RPM</small>
        </div>
        <div class="kpi-stats">
          <span>Vibración: <strong>{datoActual.vibracion ?? 1.15} mm/s</strong></span>
          <span>Potencia: <strong>{datoActual.potenciaKW ?? 92.4} kW</strong></span>
        </div>
      </div>
    </div>

    <!-- Osciloscopio Gráfico Dinámico SVG -->
    <div class="grafico-contenedor">
      <div class="grafico-header">
        <div class="grafico-titulos">
          <h3>Osciloscopio Multicanal en Tiempo Real</h3>
          <span class="stream-status" class:online={sseConectado}>
            {sseConectado ? '● STREAMING ACTIVO (1 Hz)' : '○ RECONECTANDO...'}
          </span>
        </div>
        <div class="grafico-leyenda">
          <span class="leyenda-item temp"><span class="linea temp"></span> Temperatura (°C)</span>
          <span class="leyenda-item pres"><span class="linea pres"></span> Presión (bar x 10)</span>
        </div>
      </div>

      <!-- Renderizado SVG Puro y Reactivo sin Dependencias Pesadas -->
      <div class="svg-wrapper">
        <svg viewBox="0 0 560 180" class="canvas-svg" preserveAspectRatio="none">
          <defs>
            <linearGradient id="gradTemp" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#ef4444" stop-opacity="0.25" />
              <stop offset="100%" stop-color="#ef4444" stop-opacity="0.0" />
            </linearGradient>
            <linearGradient id="gradPres" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.2" />
              <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.0" />
            </linearGradient>
          </defs>

          <!-- Rejilla milimétrica industrial -->
          <line x1="0" y1="36" x2="560" y2="36" stroke="#263342" stroke-dasharray="3,3" />
          <line x1="0" y1="90" x2="560" y2="90" stroke="#263342" stroke-dasharray="3,3" />
          <line x1="0" y1="144" x2="560" y2="144" stroke="#263342" stroke-dasharray="3,3" />

          <!-- Línea de umbral de peligro a 95°C -->
          <line x1="0" y1="45" x2="560" y2="45" stroke="#ef4444" stroke-opacity="0.4" stroke-width="1.5" />
          <text x="5" y="42" fill="#ef4444" font-size="10" font-family="monospace">UMBRAL CRÍTICO (95 °C)</text>

          <!-- Trazas de Curvas Reactivas -->
          {#if svgPuntosTemp}
            <polyline 
              fill="none" 
              stroke="#ef4444" 
              stroke-width="2.5" 
              points={svgPuntosTemp} 
            />
          {/if}

          {#if svgPuntosPresion}
            <polyline 
              fill="none" 
              stroke="#3b82f6" 
              stroke-width="2.2" 
              points={svgPuntosPresion} 
            />
          {/if}
        </svg>
      </div>

      <div class="grafico-footer">
        <span>T-25s</span>
        <span>Ventana de Muestreo Dinámico (25 segundos)</span>
        <span>Ahora ({datoActual.timestamp})</span>
      </div>
    </div>

    <!-- Bitácora de Maniobras y Eventos -->
    <div class="bitacora-caja">
      <h4>Bitácora del Servidor y Eventos Operativos</h4>
      <div class="lista-eventos">
        {#each data.planta.bitacoraEventos as ev}
          <div class="evento-fila">
            <span class="ev-time">[{ev.timestamp}]</span>
            <span class="ev-tag" class:peligro={ev.tipo === 'PELIGRO'} class:ok={ev.tipo === 'OK'}>
              {ev.tipo}
            </span>
            <span class="ev-msg">{ev.mensaje}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <!-- COLUMNA LATERAL (ACCIONES DE CONTROL Y ACTUADORES) -->
  <aside class="col-control">
    <!-- Botón de Parada de Emergencia Industrial -->
    <div class="panel-emergencia">
      <form method="POST" action="?/paradaEmergencia" use:enhance>
        <button 
          type="submit" 
          class="btn-parada-emergencia"
          disabled={data.planta.paradaEmergenciaActiva}
        >
          <span class="btn-e-icono">🛑</span>
          <span class="btn-e-texto">PARADA DE EMERGENCIA</span>
          <span class="btn-e-sub">DESCONEXIÓN INMEDIATA</span>
        </button>
      </form>
    </div>

    <!-- Ajuste de Setpoint de Presión -->
    <div class="tarjeta-control">
      <h3>Calibración de Consigna PID</h3>
      <p class="desc">Modifica el setpoint de presión con validación estricta en servidor:</p>

      <form 
        method="POST" 
        action="?/ajustarSetpoint" 
        use:enhance={() => {
          ajustandoSetpoint = true;
          return async ({ update }) => {
            ajustandoSetpoint = false;
            await update();
          };
        }}
      >
        <div class="campo-consigna">
          <label for="presion">Presión Objetivo (1.0 a 8.0 bar):</label>
          <div class="input-setpoint-row">
            <input 
              id="presion" 
              name="presion" 
              type="number" 
              step="0.1" 
              min="1.0" 
              max="8.0" 
              value={data.planta.setpointPresion} 
              required 
            />
            <span class="unidad-tag">bar</span>
          </div>
        </div>

        <button type="submit" class="btn-aplicar" disabled={ajustandoSetpoint}>
          {ajustandoSetpoint ? 'Transmitiendo...' : 'Actualizar Consigna'}
        </button>
      </form>
    </div>

    <!-- Control de Actuadores y Bombas -->
    <div class="tarjeta-control">
      <h3>Actuadores Primarios ({data.planta.actuadores.length})</h3>
      <p class="desc">Maniobras individuales con mutación directa en Form Action:</p>

      <div class="lista-actuadores">
        {#each data.planta.actuadores as act (act.id)}
          <div class="actuador-item" class:activo={act.encendido}>
            <div class="act-detalles">
              <span class="act-tag">{act.id}</span>
              <span class="act-nombre">{act.tag}</span>
              <span class="act-pot">{act.encendido ? `${act.potenciaPct}% potencia` : 'DETENIDO'}</span>
            </div>

            <form method="POST" action="?/alternarActuador" use:enhance>
              <input type="hidden" name="id" value={act.id} />
              <button 
                type="submit" 
                class="btn-switch" 
                class:on={act.encendido}
                disabled={data.planta.paradaEmergenciaActiva}
              >
                {act.encendido ? 'APAGAR' : 'ENCENDER'}
              </button>
            </form>
          </div>
        {/each}
      </div>
    </div>
  </aside>
</div>

<style>
  .dashboard-grid {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 1.5rem;
    padding: 1.75rem;
    max-width: 1400px;
    margin: 0 auto;
    width: 100%;
    box-sizing: border-box;
  }

  @media (max-width: 1024px) {
    .dashboard-grid {
      grid-template-columns: 1fr;
    }
  }

  .banner-critico {
    background: rgba(239, 68, 68, 0.15);
    border: 2px solid var(--color-danger);
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    animation: bordeParpadeo 1.5s infinite;
  }

  @keyframes bordeParpadeo {
    0%, 100% { border-color: var(--color-danger); }
    50% { border-color: rgba(239, 68, 68, 0.4); }
  }

  .critico-contenido {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .alerta-icono {
    font-size: 2rem;
  }

  .critico-contenido h3 {
    margin: 0 0 0.25rem 0;
    color: var(--color-danger);
    font-size: 1.1rem;
  }

  .critico-contenido p {
    margin: 0;
    font-size: 0.85rem;
    color: var(--text-primary);
  }

  .btn-rearmar {
    background: var(--color-success);
    color: #ffffff;
    border: none;
    padding: 0.65rem 1.25rem;
    border-radius: 6px;
    font-weight: 700;
    cursor: pointer;
    font-size: 0.85rem;
  }

  .banner-feedback {
    padding: 0.85rem 1.25rem;
    border-radius: 8px;
    margin-bottom: 1.25rem;
    font-size: 0.9rem;
    font-weight: 500;
  }

  .banner-feedback.error {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid var(--color-danger);
    color: #fca5a5;
  }

  .banner-feedback.exito {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid var(--color-success);
    color: #6ee7b7;
  }

  .kpi-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.25rem;
    margin-bottom: 1.5rem;
  }

  .kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: border-color 0.2s;
  }

  .kpi-card.alerta {
    border-color: var(--color-danger);
    background: rgba(239, 68, 68, 0.05);
  }

  .kpi-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .kpi-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 0.05em;
  }

  .kpi-badge {
    font-size: 0.65rem;
    background: var(--bg-surface);
    color: var(--text-secondary);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-family: var(--font-mono);
  }

  .kpi-valor {
    font-size: 2.3rem;
    font-weight: 700;
    color: var(--text-primary);
    font-family: var(--font-mono);
    margin: 0.5rem 0;
  }

  .kpi-valor small {
    font-size: 1.1rem;
    color: var(--text-muted);
    font-weight: 400;
  }

  .kpi-stats {
    display: flex;
    justify-content: space-between;
    border-top: 1px solid var(--border-color);
    padding-top: 0.65rem;
    font-size: 0.78rem;
    color: var(--text-secondary);
  }

  .kpi-stats strong {
    color: var(--text-primary);
  }

  .kpi-stats strong.positivo {
    color: var(--color-success);
  }

  .grafico-contenedor {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .grafico-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .grafico-titulos h3 {
    margin: 0 0 0.25rem 0;
    font-size: 1.1rem;
    color: var(--text-primary);
  }

  .stream-status {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-family: var(--font-mono);
  }

  .stream-status.online {
    color: var(--color-success);
  }

  .grafico-leyenda {
    display: flex;
    gap: 1.25rem;
    font-size: 0.8rem;
    color: var(--text-secondary);
  }

  .leyenda-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }

  .linea {
    display: inline-block;
    width: 14px;
    height: 3px;
    border-radius: 2px;
  }

  .linea.temp { background: var(--color-danger); }
  .linea.pres { background: var(--color-accent); }

  .svg-wrapper {
    background: #06090d;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 0.5rem;
    overflow: hidden;
  }

  .canvas-svg {
    width: 100%;
    height: 180px;
    display: block;
  }

  .grafico-footer {
    display: flex;
    justify-content: space-between;
    margin-top: 0.65rem;
    font-size: 0.72rem;
    color: var(--text-muted);
    font-family: var(--font-mono);
  }

  .bitacora-caja {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.25rem;
  }

  .bitacora-caja h4 {
    margin: 0 0 0.85rem 0;
    font-size: 0.85rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .lista-eventos {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    max-height: 140px;
    overflow-y: auto;
  }

  .evento-fila {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.82rem;
    padding: 0.35rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  }

  .ev-time {
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.75rem;
  }

  .ev-tag {
    font-size: 0.65rem;
    font-weight: 700;
    padding: 0.1rem 0.35rem;
    border-radius: 3px;
    background: var(--bg-surface);
    color: var(--text-secondary);
  }

  .ev-tag.peligro {
    background: rgba(239, 68, 68, 0.2);
    color: var(--color-danger);
  }

  .ev-tag.ok {
    background: rgba(16, 185, 129, 0.2);
    color: var(--color-success);
  }

  .ev-msg {
    color: var(--text-primary);
  }

  /* BARRA LATERAL */
  .col-control {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .panel-emergencia {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.25rem;
  }

  .btn-parada-emergencia {
    width: 100%;
    background: linear-gradient(180deg, #dc2626 0%, #991b1b 100%);
    border: 3px solid #f87171;
    border-radius: 10px;
    padding: 1.25rem 1rem;
    color: #ffffff;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    box-shadow: 0 6px 20px rgba(220, 38, 38, 0.4);
    transition: transform 0.1s, box-shadow 0.1s;
  }

  .btn-parada-emergencia:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(220, 38, 38, 0.6);
  }

  .btn-parada-emergencia:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    border-color: #64748b;
  }

  .btn-e-icono { font-size: 1.8rem; }
  .btn-e-texto { font-size: 1rem; font-weight: 800; letter-spacing: 0.05em; }
  .btn-e-sub { font-size: 0.68rem; opacity: 0.85; letter-spacing: 0.08em; }

  .tarjeta-control {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.35rem;
  }

  .tarjeta-control h3 {
    margin: 0 0 0.35rem 0;
    font-size: 1.05rem;
    color: var(--text-primary);
  }

  .tarjeta-control .desc {
    color: var(--text-muted);
    font-size: 0.82rem;
    margin: 0 0 1.25rem 0;
    line-height: 1.4;
  }

  .campo-consigna label {
    display: block;
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin-bottom: 0.4rem;
  }

  .input-setpoint-row {
    display: flex;
    align-items: center;
    background: #06090d;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 0 0.75rem;
    margin-bottom: 1rem;
  }

  .input-setpoint-row input {
    flex: 1;
    background: transparent;
    border: none;
    color: #ffffff;
    font-size: 1.2rem;
    font-weight: 700;
    font-family: var(--font-mono);
    padding: 0.5rem 0;
    outline: none;
  }

  .unidad-tag {
    color: var(--text-muted);
    font-size: 0.9rem;
  }

  .btn-aplicar {
    width: 100%;
    background: var(--color-accent);
    color: #ffffff;
    border: none;
    padding: 0.65rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
  }

  .btn-aplicar:hover:not(:disabled) {
    background: #2563eb;
  }

  .lista-actuadores {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .actuador-item {
    background: #06090d;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: border-color 0.2s;
  }

  .actuador-item.activo {
    border-color: rgba(16, 185, 129, 0.4);
  }

  .act-detalles {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }

  .act-tag {
    font-size: 0.65rem;
    font-family: var(--font-mono);
    color: var(--text-muted);
  }

  .act-nombre {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .act-pot {
    font-size: 0.7rem;
    color: var(--text-secondary);
  }

  .btn-switch {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
    padding: 0.35rem 0.65rem;
    border-radius: 5px;
    font-size: 0.72rem;
    font-weight: 700;
    cursor: pointer;
  }

  .btn-switch.on {
    background: rgba(16, 185, 129, 0.15);
    border-color: var(--color-success);
    color: var(--color-success);
  }

  .btn-switch:hover:not(:disabled) {
    border-color: var(--text-primary);
  }
</style>
