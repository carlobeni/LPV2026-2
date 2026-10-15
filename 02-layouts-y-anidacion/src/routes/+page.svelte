<svelte:head>
  <title>Sección 02 — Layouts y Anidación</title>
</svelte:head>

<div class="contenedor">
  <div class="hero">
    <h1>Estructura de Layouts en SvelteKit</h1>
    <p>
      Esta vista está montada dentro del <strong>Layout Raíz</strong> (<code>src/routes/+layout.svelte</code>).
      Observa cómo la barra de navegación superior y el pie de página se mantienen fijos sin recargarse.
    </p>

    <div class="panel-demostracion">
      <h3>Rutas para experimentar la jerarquía:</h3>
      
      <div class="tarjetas">
        <div class="tarjeta">
          <h4>1. Layout Anidado</h4>
          <p>La ruta <code>/control</code> tiene su propio sub-layout con una barra lateral (Sidebar) técnica.</p>
          <a href="/control" class="btn">Probar Sub-layout Admin &rarr;</a>
        </div>

        <div class="tarjeta">
          <h4>2. Reseteo de Layout con @</h4>
          <p>La ruta <code>/login</code> usa <code>+page@.svelte</code> para ocultar la barra de navegación y ocupar el 100% de la pantalla.</p>
          <a href="/login" class="btn btn-outline">Probar Reseteo @ &rarr;</a>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .contenedor {
    max-width: 900px;
    margin: 3rem auto;
    padding: 0 1.5rem;
  }

  .hero h1 {
    font-size: 2.2rem;
    color: #ffffff;
    margin-bottom: 0.5rem;
  }

  .hero p {
    color: #8b949e;
    font-size: 1.05rem;
    line-height: 1.6;
    margin-bottom: 2rem;
  }

  code {
    background: #161b22;
    color: #58a6ff;
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    font-size: 0.9em;
  }

  .panel-demostracion {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 2rem;
  }

  .panel-demostracion h3 {
    margin: 0 0 1.5rem 0;
    color: #ffffff;
  }

  .tarjetas {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
  }

  .tarjeta {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .tarjeta h4 {
    margin: 0 0 0.5rem 0;
    color: #58a6ff;
  }

  .tarjeta p {
    font-size: 0.9rem;
    color: #8b949e;
    margin-bottom: 1.5rem;
  }

  .btn {
    display: inline-block;
    background: #238636;
    color: #ffffff;
    text-decoration: none;
    padding: 0.6rem 1rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    text-align: center;
  }

  .btn:hover {
    background: #2ea043;
  }

  .btn-outline {
    background: transparent;
    border: 1px solid #30363d;
    color: #e6edf3;
  }

  .btn-outline:hover {
    background: #21262d;
    border-color: #58a6ff;
  }
</style>
