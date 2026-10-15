<script>
  import { goto } from '$app/navigation';

  // Estado reactivo con Runes de Svelte 5
  let inputId = $state('PT-100');
  let rutaDoc = $state('sensores/presion/piezorresistivo');

  function navegarADispositivo() {
    if (inputId.trim()) {
      goto(`/dispositivos/${encodeURIComponent(inputId.trim())}`);
    }
  }

  function navegarADoc() {
    if (rutaDoc.trim()) {
      goto(`/docs/${rutaDoc.trim()}`);
    }
  }
</script>

<svelte:head>
  <title>Sección 01 — Enrutamiento y Páginas en SvelteKit</title>
</svelte:head>

<div class="contenedor">
  <header class="header">
    <div class="badge">SvelteKit 2 + Svelte 5</div>
    <h1>01. Enrutamiento y Páginas</h1>
    <p class="subtitulo">Demostración interactiva de File-Based Routing para Sistemas Mecatrónicos</p>
  </header>

  <div class="grid-tarjetas">
    <!-- Tarjeta 1: Rutas Estáticas -->
    <div class="tarjeta">
      <div class="tarjeta-tag">Ruta Estática</div>
      <h3>Página Institucional</h3>
      <p>Mapeo directo de carpeta física a ruta del navegador: <code>src/routes/about/+page.svelte</code></p>
      <div class="acciones">
        <a href="/about" class="btn btn-primario" data-sveltekit-preload-data="hover">
          Ir a /about &rarr;
        </a>
      </div>
    </div>

    <!-- Tarjeta 2: Rutas Dinámicas [id] -->
    <div class="tarjeta">
      <div class="tarjeta-tag dinamica">Ruta Dinámica [id]</div>
      <h3>Panel de Dispositivo Específico</h3>
      <p>Parámetros en corchetes <code>src/routes/dispositivos/[id]/+page.svelte</code>:</p>
      
      <div class="input-grupo">
        <label for="id-input">ID o Tag del Sensor:</label>
        <div class="row">
          <input 
            id="id-input" 
            type="text" 
            bind:value={inputId} 
            placeholder="ej. PT-100, MOTOR-B1, CAUDAL-4" 
          />
          <button onclick={navegarADispositivo} class="btn btn-secundario">
            Navegar con goto()
          </button>
        </div>
      </div>

      <div class="enlaces-rapidos">
        <span>Enlaces rápidos:</span>
        <a href="/dispositivos/TEMPERATURA-01">TEMPERATURA-01</a>
        <a href="/dispositivos/ENCODER-OPTICO-X">ENCODER-OPTICO-X</a>
        <a href="/dispositivos/ACC-3EJES-Z">ACC-3EJES-Z</a>
      </div>
    </div>

    <!-- Tarjeta 3: Rutas Rest [...slug] -->
    <div class="tarjeta">
      <div class="tarjeta-tag comodin">Ruta Comodín [...slug]</div>
      <h3>Documentación y Manuales Jerárquicos</h3>
      <p>Captura múltiples segmentos anidados en una sola vista: <code>src/routes/docs/[...slug]/+page.svelte</code></p>
      
      <div class="input-grupo">
        <label for="doc-input">Ruta del Manual:</label>
        <div class="row">
          <input 
            id="doc-input" 
            type="text" 
            bind:value={rutaDoc} 
            placeholder="ej. actuadores/servomotores/sg90" 
          />
          <button onclick={navegarADoc} class="btn btn-secundario">
            Ver Documento
          </button>
        </div>
      </div>

      <div class="enlaces-rapidos">
        <span>Rutas de prueba:</span>
        <a href="/docs/protocolos/can-bus/tramas">Protocolo CAN-Bus</a>
        <a href="/docs/motores/paso-a-paso/nema-17">NEMA 17</a>
      </div>
    </div>
  </div>
</div>

<style>
  :global(body) {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
    margin: 0;
    padding: 0;
  }

  .contenedor {
    max-width: 1000px;
    margin: 0 auto;
    padding: 2.5rem 1.5rem;
  }

  .header {
    text-align: center;
    margin-bottom: 3rem;
  }

  .badge {
    display: inline-block;
    padding: 0.35rem 0.85rem;
    font-size: 0.8rem;
    font-weight: 700;
    color: #ff3e00;
    background-color: rgba(255, 62, 0, 0.12);
    border: 1px solid rgba(255, 62, 0, 0.3);
    border-radius: 9999px;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  h1 {
    font-size: 2.3rem;
    margin: 0 0 0.5rem 0;
    color: #ffffff;
  }

  .subtitulo {
    color: #8b949e;
    font-size: 1.1rem;
    margin: 0;
  }

  .grid-tarjetas {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .tarjeta {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.75rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.2s ease, border-color 0.2s ease;
  }

  .tarjeta:hover {
    border-color: #58a6ff;
    transform: translateY(-2px);
  }

  .tarjeta-tag {
    align-self: flex-start;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    background: #238636;
    color: #ffffff;
    margin-bottom: 0.75rem;
  }

  .tarjeta-tag.dinamica {
    background: #1f6feb;
  }

  .tarjeta-tag.comodin {
    background: #8957e5;
  }

  h3 {
    margin: 0 0 0.5rem 0;
    color: #ffffff;
    font-size: 1.25rem;
  }

  p {
    color: #8b949e;
    font-size: 0.92rem;
    line-height: 1.5;
    margin: 0 0 1.25rem 0;
  }

  code {
    background: #0d1117;
    color: #58a6ff;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 0.85em;
  }

  .input-grupo {
    margin-bottom: 1rem;
  }

  label {
    display: block;
    font-size: 0.8rem;
    color: #8b949e;
    margin-bottom: 0.4rem;
  }

  .row {
    display: flex;
    gap: 0.5rem;
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
    transition: border-color 0.2s;
  }

  input:focus {
    border-color: #58a6ff;
  }

  .btn {
    display: inline-block;
    padding: 0.55rem 1rem;
    font-size: 0.9rem;
    font-weight: 600;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    text-decoration: none;
    text-align: center;
    transition: background-color 0.2s, opacity 0.2s;
  }

  .btn-primario {
    background-color: #238636;
    color: #ffffff;
    width: 100%;
    box-sizing: border-box;
  }

  .btn-primario:hover {
    background-color: #2ea043;
  }

  .btn-secundario {
    background-color: #21262d;
    color: #e6edf3;
    border: 1px solid #30363d;
    white-space: nowrap;
  }

  .btn-secundario:hover {
    background-color: #30363d;
  }

  .enlaces-rapidos {
    font-size: 0.8rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    align-items: center;
    margin-top: 0.75rem;
    border-top: 1px solid #21262d;
    padding-top: 0.75rem;
  }

  .enlaces-rapidos span {
    color: #8b949e;
  }

  .enlaces-rapidos a {
    color: #58a6ff;
    text-decoration: none;
  }

  .enlaces-rapidos a:hover {
    text-decoration: underline;
  }
</style>
