<svelte:head>
  <title>Acerca de — SvelteKit Routing</title>
</svelte:head>

<div class="contenedor">
  <div class="tarjeta-info">
    <a href="/" class="volver">&larr; Volver a la raíz</a>
    <span class="etiqueta">Ruta Estática: /about</span>
    
    <h1>Laboratorio de Lenguajes de Programación Visual</h1>
    <h2>Facultad de Ingeniería — Universidad Nacional de Asunción</h2>

    <p>
      Esta página ejemplifica el funcionamiento de una <strong>ruta estática</strong> en SvelteKit.
      El archivo físico se encuentra en:
    </p>
    <code>src/routes/about/+page.svelte</code>

    <div class="detalles">
      <h3>Características de las Rutas Estáticas:</h3>
      <ul>
        <li><strong>Predecibles:</strong> La URL refleja 1:1 el árbol de carpetas.</li>
        <li><strong>Optimizadas para SEO:</strong> El servidor entrega el HTML completamente renderizado (SSR).</li>
        <li><strong>Fácilmente pre-renderizables:</strong> Con <code>export const prerender = true;</code> pueden compilarse a HTML puro para CDNs sin coste de cómputo en servidor.</li>
      </ul>
    </div>
  </div>
</div>

<style>
  .contenedor {
    max-width: 750px;
    margin: 3rem auto;
    padding: 1.5rem;
  }

  .tarjeta-info {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 2.5rem;
  }

  .volver {
    display: inline-block;
    color: #58a6ff;
    text-decoration: none;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
    transition: color 0.2s;
  }

  .volver:hover {
    text-decoration: underline;
  }

  .etiqueta {
    display: block;
    font-size: 0.75rem;
    font-weight: 700;
    color: #238636;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
  }

  h1 {
    font-size: 1.8rem;
    color: #ffffff;
    margin: 0 0 0.5rem 0;
  }

  h2 {
    font-size: 1.1rem;
    color: #8b949e;
    font-weight: 400;
    margin: 0 0 1.5rem 0;
  }

  p {
    color: #c9d1d9;
    line-height: 1.6;
    margin-bottom: 1rem;
  }

  code {
    display: block;
    background: #0d1117;
    color: #58a6ff;
    padding: 0.75rem 1rem;
    border-radius: 6px;
    border: 1px solid #30363d;
    font-family: ui-monospace, monospace;
    font-size: 0.9rem;
    margin-bottom: 2rem;
  }

  .detalles {
    border-top: 1px solid #30363d;
    padding-top: 1.5rem;
  }

  h3 {
    color: #ffffff;
    font-size: 1.1rem;
    margin: 0 0 0.75rem 0;
  }

  ul {
    padding-left: 1.25rem;
    color: #8b949e;
  }

  li {
    margin-bottom: 0.5rem;
    line-height: 1.5;
  }

  li strong {
    color: #e6edf3;
  }
</style>
