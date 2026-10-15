<script>
  import { page } from '$app/state';

  let { data, children } = $props();
</script>

<div class="scada-shell">
  <!-- Cabecera Superior de Planta -->
  <header class="scada-header">
    <div class="marca">
      <div class="logo-box">
        <span class="pulsar"></span>
        <span class="logo-icon">🏭</span>
      </div>
      <div class="titulos">
        <span class="sistema-tag">FIUNA · MECATRÓNICA · SCADA</span>
        <h1>Plataforma de Telemetría y Control de Planta</h1>
      </div>
    </div>

    <nav class="nav-links">
      <a href="/" class:activo={page.url.pathname === '/'}>
        📊 Dashboard en Vivo
      </a>
      <a href="/about" class:activo={page.url.pathname === '/about'}>
        ℹ️ Arquitectura del Sistema
      </a>
      <a href="/api/exportar" class="btn-exportar">
        📥 Exportar Auditoría (.csv)
      </a>
    </nav>

    <div class="panel-usuario">
      <div class="usuario-badge">
        <span class="rol-dot" class:admin={data.usuario?.rol === 'ingeniero_jefe'}></span>
        <div class="usr-textos">
          <span class="usr-nombre">{data.usuario?.nombre}</span>
          <span class="usr-rol">{data.usuario?.rol?.replace('_', ' ').toUpperCase()}</span>
        </div>
      </div>
      <span class="nodo-tag">{data.nodoId}</span>
    </div>
  </header>

  <!-- Contenedor Principal -->
  <main class="scada-body">
    {@render children()}
  </main>

  <!-- Barra de Estado Inferior -->
  <footer class="scada-footer">
    <div class="footer-left">
      <span class="status-indicator online"></span>
      <span>Bus CAN 2.0B / Modbus TCP: <strong>SINCRONIZADO (100 Hz)</strong></span>
    </div>
    <div class="footer-center">
      <span>Lenguajes de Programación Visual 2026-2 · SvelteKit 2 + Svelte 5 (Runes Mode)</span>
    </div>
    <div class="footer-right">
      <span>{data.versionSistema}</span>
    </div>
  </footer>
</div>

<style>
  :global(:root) {
    --bg-main: #0a0e14;
    --bg-card: #121820;
    --bg-surface: #1a222d;
    --border-color: #263342;
    --border-hover: #3b82f6;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --color-accent: #3b82f6;
    --color-success: #10b981;
    --color-warning: #f59e0b;
    --color-danger: #ef4444;
    --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  }

  :global(body) {
    margin: 0;
    padding: 0;
    background-color: var(--bg-main);
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }

  .scada-shell {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .scada-header {
    height: 68px;
    background: var(--bg-card);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 1.75rem;
    position: sticky;
    top: 0;
    z-index: 50;
  }

  .marca {
    display: flex;
    align-items: center;
    gap: 0.85rem;
  }

  .logo-box {
    position: relative;
    width: 38px;
    height: 38px;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
  }

  .pulsar {
    position: absolute;
    top: -2px;
    right: -2px;
    width: 8px;
    height: 8px;
    background: var(--color-success);
    border-radius: 50%;
    box-shadow: 0 0 8px var(--color-success);
    animation: pulso 2s infinite;
  }

  @keyframes pulso {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(1.3); }
  }

  .titulos h1 {
    font-size: 1.05rem;
    margin: 0;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
  }

  .sistema-tag {
    display: block;
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--color-accent);
    letter-spacing: 0.08em;
  }

  .nav-links {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .nav-links a {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 500;
    padding: 0.45rem 0.85rem;
    border-radius: 6px;
    transition: all 0.2s;
  }

  .nav-links a:hover {
    color: var(--text-primary);
    background: var(--bg-surface);
  }

  .nav-links a.activo {
    color: #ffffff;
    background: rgba(59, 130, 246, 0.2);
    border: 1px solid rgba(59, 130, 246, 0.4);
  }

  .btn-exportar {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-color) !important;
    color: var(--color-accent) !important;
  }

  .panel-usuario {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .usuario-badge {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    padding: 0.35rem 0.75rem;
    border-radius: 20px;
  }

  .rol-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--color-accent);
  }

  .rol-dot.admin {
    background: #a855f7;
    box-shadow: 0 0 6px #a855f7;
  }

  .usr-textos {
    display: flex;
    flex-direction: column;
  }

  .usr-nombre {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .usr-rol {
    font-size: 0.62rem;
    color: var(--text-muted);
    font-weight: 600;
    letter-spacing: 0.04em;
  }

  .nodo-tag {
    font-size: 0.7rem;
    font-family: var(--font-mono);
    color: var(--text-muted);
    background: #06090d;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    border: 1px solid var(--border-color);
  }

  .scada-body {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .scada-footer {
    height: 38px;
    background: var(--bg-card);
    border-top: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 1.5rem;
    font-size: 0.75rem;
    color: var(--text-muted);
  }

  .footer-left {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .status-indicator {
    width: 6px;
    height: 6px;
    border-radius: 50%;
  }

  .status-indicator.online {
    background: var(--color-success);
    box-shadow: 0 0 6px var(--color-success);
  }
</style>
