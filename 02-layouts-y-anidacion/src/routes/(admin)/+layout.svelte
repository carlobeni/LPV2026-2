<script>
  let { children } = $props();

  // Simulación de actuadores en el sidebar de control
  let actuadores = $state([
    { nombre: 'Bomba Hidráulica 1', activo: true },
    { nombre: 'Servoválvula Proporcional', activo: false },
    { nombre: 'Calentador Reactor', activo: true }
  ]);
</script>

<div class="admin-shell">
  <!-- Barra lateral exclusiva de la sección administrativa -->
  <aside class="sidebar-admin">
    <div class="sidebar-header">
      <span class="etiqueta-sublayout">SUB-LAYOUT ADMIN</span>
      <h3>Consola de Planta</h3>
    </div>

    <div class="seccion-actuadores">
      <h4>Actuadores en Línea</h4>
      <ul>
        {#each actuadores as act, i}
          <li>
            <span class="led" class:on={act.activo}></span>
            <span class="nombre">{act.nombre}</span>
            <button 
              class="btn-toggle" 
              onclick={() => act.activo = !act.activo}
            >
              {act.activo ? 'PARAR' : 'ARRANCAR'}
            </button>
          </li>
        {/each}
      </ul>
    </div>

    <div class="sidebar-footer">
      <a href="/" class="link-retorno">&larr; Volver al Inicio</a>
    </div>
  </aside>

  <!-- Contenido de las páginas hijas de (admin) -->
  <section class="admin-viewport">
    {@render children()}
  </section>
</div>

<style>
  .admin-shell {
    display: flex;
    flex: 1;
    min-height: calc(100vh - 60px - 48px);
  }

  .sidebar-admin {
    width: 280px;
    background: #161b22;
    border-right: 1px solid #30363d;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .etiqueta-sublayout {
    font-size: 0.65rem;
    font-weight: 700;
    color: #8957e5;
    background: rgba(137, 87, 229, 0.15);
    border: 1px solid rgba(137, 87, 229, 0.3);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    letter-spacing: 0.05em;
  }

  .sidebar-header h3 {
    margin: 0.75rem 0 1.5rem 0;
    font-size: 1.15rem;
    color: #ffffff;
  }

  .seccion-actuadores h4 {
    font-size: 0.75rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 0.75rem 0;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  li {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 6px;
    padding: 0.6rem 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.85rem;
  }

  .led {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #484f58;
  }

  .led.on {
    background: #3fb950;
    box-shadow: 0 0 6px rgba(63, 185, 80, 0.8);
  }

  .nombre {
    flex: 1;
    color: #c9d1d9;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .btn-toggle {
    background: #21262d;
    border: 1px solid #30363d;
    color: #8b949e;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.7rem;
    cursor: pointer;
  }

  .btn-toggle:hover {
    color: #ffffff;
    border-color: #58a6ff;
  }

  .link-retorno {
    color: #58a6ff;
    font-size: 0.85rem;
    text-decoration: none;
  }

  .link-retorno:hover {
    text-decoration: underline;
  }

  .admin-viewport {
    flex: 1;
    background: #0d1117;
    padding: 2rem;
  }
</style>
