<script>
  import { enhance } from '$app/forms';

  // Desestructuramos datos del servidor y feedback del formulario
  let { data, form } = $props();

  // Estados locales con Runes para feedback de carga interactivo
  let creando = $state(false);
  let idEnCalibracion = $state(null);
  let idEnEliminacion = $state(null);
</script>

<svelte:head>
  <title>04. Form Actions y Mutaciones con use:enhance</title>
</svelte:head>

<div class="contenedor">
  <header class="header">
    <span class="badge">SvelteKit Form Actions</span>
    <h1>Gestión y Mutación de Sensores</h1>
    <p class="sub">Demostración de Progressive Enhancement y validación segura en servidor</p>
  </header>

  <!-- Mensajes de feedback del servidor -->
  {#if form?.error}
    <div class="banner-error">
      ❌ {form.error}
    </div>
  {/if}

  {#if form?.exito}
    <div class="banner-exito">
      ✅ {form.mensaje}
    </div>
  {/if}

  <div class="grid-principal">
    <!-- Formulario de creación -->
    <div class="tarjeta-form">
      <h3>Alta de Nuevo Instrumento</h3>
      <p class="desc">Formulario HTML nativo potenciado con <code>use:enhance</code>:</p>

      <form 
        method="POST" 
        action="?/crear" 
        use:enhance={() => {
          creando = true;
          return async ({ update }) => {
            creando = false;
            await update({ reset: form?.exito ?? true });
          };
        }}
      >
        <div class="campo">
          <label for="tag">Tag del Instrumento:</label>
          <input 
            id="tag" 
            name="tag" 
            type="text" 
            placeholder="ej. PT100-HORNO-2" 
            value={form?.campos?.tag ?? ''} 
            required 
          />
        </div>

        <div class="campo">
          <label for="tipo">Magnitud / Tipo:</label>
          <select id="tipo" name="tipo">
            <option value="Temperatura">Temperatura (°C)</option>
            <option value="Presión">Presión (bar)</option>
            <option value="Flujo">Flujo Másico (kg/h)</option>
            <option value="Vibración">Aceleración (m/s²)</option>
          </select>
        </div>

        <div class="campo">
          <label for="valorInicial">Valor Inicial de Calibración:</label>
          <input 
            id="valorInicial" 
            name="valorInicial" 
            type="number" 
            step="0.01" 
            placeholder="0.00" 
            value={form?.campos?.valorInicial ?? '0.00'} 
            required 
          />
        </div>

        <button type="submit" class="btn-crear" disabled={creando}>
          {#if creando}
            <span class="spinner"></span> Registrando en Planta...
          {:else}
            Registrar Instrumento (+POST)
          {/if}
        </button>
      </form>
    </div>

    <!-- Lista de inventario con acciones por elemento -->
    <div class="tarjeta-lista">
      <h3>Instrumentos Activos en el Bus ({data.sensores.length})</h3>

      <div class="lista-items">
        {#each data.sensores as sensor (sensor.id)}
          <div class="item-sensor">
            <div class="item-info">
              <span class="id-badge">{sensor.id}</span>
              <h4>{sensor.tag}</h4>
              <p>{sensor.tipo} — <strong>{sensor.valor}</strong></p>
              <span class="cal-badge" class:calibrado={sensor.calibrado}>
                {sensor.calibrado ? 'CALIBRADO' : 'PENDIENTE CALIBRACIÓN'}
              </span>
            </div>

            <div class="item-acciones">
              <!-- Acción nominada calibrar -->
              <form 
                method="POST" 
                action="?/calibrar" 
                use:enhance={() => {
                  idEnCalibracion = sensor.id;
                  return async ({ update }) => {
                    idEnCalibracion = null;
                    await update();
                  };
                }}
              >
                <input type="hidden" name="id" value={sensor.id} />
                <button 
                  type="submit" 
                  class="btn-cal" 
                  disabled={sensor.calibrado || idEnCalibracion === sensor.id}
                >
                  {idEnCalibracion === sensor.id ? 'Calibrando...' : 'Calibrar'}
                </button>
              </form>

              <!-- Acción nominada eliminar -->
              <form 
                method="POST" 
                action="?/eliminar" 
                use:enhance={() => {
                  idEnEliminacion = sensor.id;
                  return async ({ update }) => {
                    idEnEliminacion = null;
                    await update();
                  };
                }}
              >
                <input type="hidden" name="id" value={sensor.id} />
                <button 
                  type="submit" 
                  class="btn-del" 
                  disabled={idEnEliminacion === sensor.id}
                >
                  {idEnEliminacion === sensor.id ? 'Borrando...' : 'Eliminar'}
                </button>
              </form>
            </div>
          </div>
        {:else}
          <p class="vacio">No hay instrumentos en el inventario.</p>
        {/each}
      </div>
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
    max-width: 1050px;
    margin: 2.5rem auto;
    padding: 0 1.5rem;
  }

  .badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: #ff3e00;
    background: rgba(255, 62, 0, 0.12);
    border-radius: 9999px;
    margin-bottom: 0.75rem;
    text-transform: uppercase;
  }

  h1 {
    font-size: 2.2rem;
    margin: 0 0 0.5rem 0;
    color: #ffffff;
  }

  .sub {
    color: #8b949e;
    margin: 0 0 1.75rem 0;
  }

  .banner-error {
    background: rgba(248, 81, 73, 0.15);
    border: 1px solid #f85149;
    color: #ff7b72;
    padding: 0.85rem 1.25rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
  }

  .banner-exito {
    background: rgba(63, 185, 80, 0.15);
    border: 1px solid #3fb950;
    color: #56d364;
    padding: 0.85rem 1.25rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
  }

  .grid-principal {
    display: grid;
    grid-template-columns: 1fr 1.3fr;
    gap: 1.75rem;
  }

  @media (max-width: 800px) {
    .grid-principal {
      grid-template-columns: 1fr;
    }
  }

  .tarjeta-form, .tarjeta-lista {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.75rem;
  }

  h3 {
    margin: 0 0 0.4rem 0;
    color: #ffffff;
    font-size: 1.2rem;
  }

  .desc {
    color: #8b949e;
    font-size: 0.85rem;
    margin: 0 0 1.5rem 0;
  }

  code {
    color: #58a6ff;
  }

  .campo {
    margin-bottom: 1.25rem;
  }

  label {
    display: block;
    font-size: 0.8rem;
    color: #8b949e;
    margin-bottom: 0.4rem;
  }

  input, select {
    width: 100%;
    box-sizing: border-box;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #e6edf3;
    padding: 0.6rem 0.75rem;
    font-size: 0.9rem;
    outline: none;
  }

  input:focus, select:focus {
    border-color: #58a6ff;
  }

  .btn-crear {
    width: 100%;
    background: #238636;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 0.75rem;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .btn-crear:hover:not(:disabled) {
    background: #2ea043;
  }

  .btn-crear:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .spinner {
    width: 14px;
    height: 14px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: giro 0.6s linear infinite;
  }

  @keyframes giro {
    to { transform: rotate(360deg); }
  }

  .lista-items {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
  }

  .item-sensor {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .id-badge {
    font-size: 0.7rem;
    font-weight: 700;
    color: #8957e5;
  }

  .item-info h4 {
    margin: 0.2rem 0;
    color: #ffffff;
    font-size: 1.05rem;
  }

  .item-info p {
    margin: 0 0 0.35rem 0;
    color: #8b949e;
    font-size: 0.85rem;
  }

  .cal-badge {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    background: #484f58;
    color: #c9d1d9;
  }

  .cal-badge.calibrado {
    background: rgba(63, 185, 80, 0.15);
    color: #3fb950;
  }

  .item-acciones {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }

  .btn-cal {
    background: #21262d;
    border: 1px solid #30363d;
    color: #58a6ff;
    padding: 0.35rem 0.75rem;
    border-radius: 4px;
    font-size: 0.75rem;
    cursor: pointer;
  }

  .btn-cal:hover:not(:disabled) {
    background: #30363d;
  }

  .btn-cal:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .btn-del {
    background: rgba(248, 81, 73, 0.1);
    border: 1px solid rgba(248, 81, 73, 0.3);
    color: #ff7b72;
    padding: 0.35rem 0.75rem;
    border-radius: 4px;
    font-size: 0.75rem;
    cursor: pointer;
  }

  .btn-del:hover:not(:disabled) {
    background: rgba(248, 81, 73, 0.25);
  }
</style>
