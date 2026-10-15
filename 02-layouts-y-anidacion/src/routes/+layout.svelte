<script>
  import { page } from '$app/state';

  // En Svelte 5 se extrae 'children' con la runa $props()
  let { children } = $props();

  // Estado reactivo para simulación de bus en el layout
  let busConectado = $state(true);
</script>

<div class="layout-raiz">
  <!-- Barra de navegación persistente -->
  <header class="navbar">
    <div class="nav-marca">
      <span class="icono">⚡</span>
      <span class="texto">FIUNA <strong>Telemetría</strong></span>
    </div>

    <nav class="nav-links">
      <a href="/" class:activo={page.url.pathname === '/'}>Inicio</a>
      <a href="/control" class:activo={page.url.pathname.startsWith('/control')}>Panel Admin</a>
      <a href="/login" class:activo={page.url.pathname === '/login'}>Acceso (Full)</a>
    </nav>

    <div class="nav-estado">
      <span class="punto-estado" class:conectado={busConectado}></span>
      <span class="estado-label">{busConectado ? 'BUS ACTIVO' : 'OFFLINE'}</span>
    </div>
  </header>

  <!-- Área de contenido dinámico -->
  <main class="contenido-principal">
    {@render children()}
  </main>

  <!-- Pie de página persistente -->
  <footer class="footer">
    <p>Lenguajes de Programación Visual · FIUNA 2026-2 · SvelteKit 2 Layout Hierarchy</p>
  </footer>
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    background-color: #0d1117;
    color: #e6edf3;
    font-family: system-ui, -apple-system, sans-serif;
  }

  .layout-raiz {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .navbar {
    height: 60px;
    background: #161b22;
    border-bottom: 1px solid #30363d;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 1.5rem;
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .nav-marca {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.1rem;
    color: #ffffff;
  }

  .nav-marca .icono {
    color: #ff3e00;
  }

  .nav-links {
    display: flex;
    gap: 1.25rem;
  }

  .nav-links a {
    color: #8b949e;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    padding: 0.35rem 0.6rem;
    border-radius: 6px;
    transition: color 0.2s, background 0.2s;
  }

  .nav-links a:hover {
    color: #ffffff;
    background: #21262d;
  }

  .nav-links a.activo {
    color: #58a6ff;
    background: rgba(88, 166, 255, 0.1);
  }

  .nav-estado {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    font-weight: 600;
  }

  .punto-estado {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #f85149;
  }

  .punto-estado.conectado {
    background-color: #3fb950;
    box-shadow: 0 0 8px rgba(63, 185, 80, 0.6);
  }

  .estado-label {
    color: #8b949e;
    letter-spacing: 0.05em;
  }

  .contenido-principal {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .footer {
    height: 48px;
    background: #0d1117;
    border-top: 1px solid #21262d;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #6e7681;
    font-size: 0.8rem;
  }
</style>
