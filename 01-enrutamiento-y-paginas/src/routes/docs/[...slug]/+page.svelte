<script>
  import { page } from '$app/state';

  // El parámetro rest slug captura todos los segmentos como una sola cadena
  let slug = $derived(page.params.slug);
  
  // Segmentos individuales separados por barra
  let segmentos = $derived(slug ? slug.split('/') : []);
</script>

<svelte:head>
  <title>Docs: {slug} — Manual Técnico</title>
</svelte:head>

<div class="contenedor">
  <div class="tarjeta-doc">
    <a href="/" class="volver">&larr; Volver al menú principal</a>

    <header class="doc-header">
      <span class="badge-comodin">Ruta Comodín: [...slug]</span>
      <h1>Documentación Técnica</h1>
      <p class="descripcion">
        Ruta definida en: <code>src/routes/docs/[...slug]/+page.svelte</code>
      </p>
    </header>

    <nav class="breadcrumbs" aria-label="Breadcrumb">
      <span class="migaja"><a href="/">inicio</a></span>
      <span class="separador">/</span>
      <span class="migaja"><a href="/docs/indice">docs</a></span>
      {#each segmentos as seg, i}
        <span class="separador">/</span>
        <span class="migaja" class:activa={i === segmentos.length - 1}>
          {seg}
        </span>
      {/each}
    </nav>

    <div class="caja-tecnica">
      <h3>Desglose del Segmento Rest:</h3>
      <table class="tabla-segmentos">
        <thead>
          <tr>
            <th>Nivel</th>
            <th>Segmento</th>
            <th>Significado en Jerarquía</th>
          </tr>
        </thead>
        <tbody>
          {#each segmentos as seg, idx}
            <tr>
              <td><code>Nivel {idx + 1}</code></td>
              <td class="resaltado">{seg}</td>
              <td>{idx === 0 ? 'Categoría principal' : idx === 1 ? 'Subcategoría de equipo' : 'Elemento específico'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <div class="simulacion-contenido">
      <h3>Contenido del Documento Técnico:</h3>
      <p>
        Has accedido a la especificación de <strong>{slug}</strong>. 
        En una aplicación real, esta ruta puede cargar archivos Markdown correspondientes a esa ruta de carpetas usando <code>import.meta.glob</code> o una base de datos documental.
      </p>
    </div>
  </div>
</div>

<style>
  .contenedor {
    max-width: 850px;
    margin: 3rem auto;
    padding: 1.5rem;
  }

  .tarjeta-doc {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 2.25rem;
  }

  .volver {
    display: inline-block;
    color: #58a6ff;
    text-decoration: none;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
  }

  .volver:hover {
    text-decoration: underline;
  }

  .badge-comodin {
    display: inline-block;
    background: #8957e5;
    color: #ffffff;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    margin-bottom: 0.5rem;
  }

  h1 {
    font-size: 1.9rem;
    color: #ffffff;
    margin: 0 0 0.5rem 0;
  }

  .descripcion {
    color: #8b949e;
    margin: 0 0 1.5rem 0;
    font-size: 0.95rem;
  }

  code {
    background: #0d1117;
    color: #f0883e;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-family: ui-monospace, monospace;
    font-size: 0.85em;
  }

  .breadcrumbs {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.4rem;
    background: #0d1117;
    padding: 0.75rem 1rem;
    border-radius: 6px;
    border: 1px solid #30363d;
    margin-bottom: 1.75rem;
    font-size: 0.9rem;
  }

  .breadcrumbs a {
    color: #58a6ff;
    text-decoration: none;
  }

  .breadcrumbs a:hover {
    text-decoration: underline;
  }

  .separador {
    color: #6e7681;
  }

  .migaja.activa {
    color: #ffffff;
    font-weight: 600;
  }

  .caja-tecnica {
    margin-bottom: 1.75rem;
  }

  .caja-tecnica h3 {
    font-size: 1.1rem;
    color: #ffffff;
    margin: 0 0 0.75rem 0;
  }

  .tabla-segmentos {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
    text-align: left;
  }

  .tabla-segmentos th, .tabla-segmentos td {
    padding: 0.6rem 0.75rem;
    border: 1px solid #30363d;
  }

  .tabla-segmentos th {
    background: #21262d;
    color: #e6edf3;
  }

  .tabla-segmentos td {
    color: #8b949e;
  }

  .tabla-segmentos td.resaltado {
    color: #58a6ff;
    font-weight: 600;
  }

  .simulacion-contenido {
    background: #21262d;
    border-left: 4px solid #8957e5;
    padding: 1.25rem;
    border-radius: 0 8px 8px 0;
  }

  .simulacion-contenido h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
    color: #ffffff;
  }

  .simulacion-contenido p {
    margin: 0;
    color: #c9d1d9;
    line-height: 1.5;
    font-size: 0.9rem;
  }
</style>
