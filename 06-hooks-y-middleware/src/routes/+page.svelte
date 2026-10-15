<script>
  import { page } from '$app/state';

  let { data } = $props();

  let alerta = $derived(page.url.searchParams.get('alerta'));
</script>

<svelte:head>
  <title>06. Hooks de Servidor y Middleware</title>
</svelte:head>

<div class="contenedor">
  <header class="header">
    <span class="badge">SvelteKit hooks.server.js</span>
    <h1>Control de Acceso y Middleware Global</h1>
    <p class="sub">Interceptación de sesiones, inyección en event.locals y protección de rutas críticas</p>
  </header>

  {#if alerta === 'debe_iniciar_sesion'}
    <div class="banner-alerta">
      ⛔ <strong>Acceso Bloqueado por Hook:</strong> Debes autenticarte antes de ingresar a la zona de calibración.
    </div>
  {:else if alerta === 'acceso_denegado_requiere_admin'}
    <div class="banner-alerta prohibido">
      🚫 <strong>Permisos Insuficientes:</strong> Tu rol actual (operador) no tiene privilegios para acceder al panel de administración.
    </div>
  {/if}

  <div class="tarjeta-sesion">
    <h3>Estado de la Sesión Actual (leído desde <code>data.usuario</code>):</h3>

    {#if data.usuario}
      <div class="usuario-conectado">
        <div class="avatar">👤</div>
        <div class="info">
          <h4>{data.usuario.nombre}</h4>
          <span class="rol-badge" class:admin={data.usuario.rol === 'administrador'}>
            ROL: {data.usuario.rol.toUpperCase()}
          </span>
          <p class="id">ID de Operario: <code>{data.usuario.id}</code></p>
        </div>

        <form method="POST" action="?/cerrarSesion" class="form-logout">
          <button type="submit" class="btn-logout">Cerrar Sesión</button>
        </form>
      </div>
    {:else}
      <div class="usuario-anonimo">
        <p>No hay ninguna sesión activa en las cookies del navegador (<code>locals.user === null</code>).</p>
        
        <div class="botones-login">
          <form method="POST" action="?/iniciarOperador">
            <button type="submit" class="btn-login op">
              Iniciar como Operador de Turno
            </button>
          </form>

          <form method="POST" action="?/iniciarAdmin">
            <button type="submit" class="btn-login adm">
              Iniciar como Administrador (Ingeniero)
            </button>
          </form>
        </div>
      </div>
    {/if}
  </div>

  <div class="tarjeta-rutas-prueba">
    <h3>Prueba de Interceptación de Rutas con el Hook:</h3>
    <p>
      El archivo <code>src/hooks.server.js</code> intercepta las peticiones dirigidas a <code>/admin/*</code>.
      Intenta acceder con cada estado de sesión para verificar el comportamiento:
    </p>

    <div class="enlaces-prueba">
      <a href="/admin/calibracion-segura" class="btn-ir-admin">
        Intentar acceder a /admin/calibracion-segura &rarr;
      </a>
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
    max-width: 850px;
    margin: 2.5rem auto;
    padding: 0 1.5rem;
  }

  .badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: #a371f7;
    background: rgba(163, 113, 247, 0.12);
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

  .banner-alerta {
    background: rgba(210, 153, 34, 0.15);
    border: 1px solid #d29922;
    color: #e3b341;
    padding: 0.85rem 1.25rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
  }

  .banner-alerta.prohibido {
    background: rgba(248, 81, 73, 0.15);
    border-color: #f85149;
    color: #ff7b72;
  }

  .tarjeta-sesion, .tarjeta-rutas-prueba {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.75rem;
    margin-bottom: 1.5rem;
  }

  h3 {
    margin: 0 0 1.25rem 0;
    font-size: 1.15rem;
    color: #ffffff;
  }

  code {
    color: #58a6ff;
  }

  .usuario-conectado {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 1.25rem;
  }

  .avatar {
    font-size: 2.2rem;
  }

  .info {
    flex: 1;
  }

  .info h4 {
    margin: 0 0 0.35rem 0;
    color: #ffffff;
    font-size: 1.1rem;
  }

  .rol-badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    background: #1f6feb;
    color: #ffffff;
    margin-bottom: 0.4rem;
  }

  .rol-badge.admin {
    background: #8957e5;
  }

  .id {
    margin: 0;
    font-size: 0.8rem;
    color: #8b949e;
  }

  .btn-logout {
    background: #21262d;
    border: 1px solid #30363d;
    color: #ff7b72;
    padding: 0.5rem 0.85rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 600;
  }

  .btn-logout:hover {
    background: rgba(248, 81, 73, 0.2);
  }

  .usuario-anonimo p {
    color: #8b949e;
    margin: 0 0 1.25rem 0;
  }

  .botones-login {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .btn-login {
    border: none;
    padding: 0.65rem 1rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    color: #ffffff;
    transition: opacity 0.2s;
  }

  .btn-login.op {
    background: #1f6feb;
  }

  .btn-login.adm {
    background: #8957e5;
  }

  .btn-login:hover {
    opacity: 0.9;
  }

  .tarjeta-rutas-prueba p {
    color: #8b949e;
    line-height: 1.5;
    margin-bottom: 1.25rem;
  }

  .btn-ir-admin {
    display: inline-block;
    background: #238636;
    color: #ffffff;
    text-decoration: none;
    font-weight: 600;
    padding: 0.65rem 1.25rem;
    border-radius: 6px;
    font-size: 0.9rem;
  }

  .btn-ir-admin:hover {
    background: #2ea043;
  }
</style>
