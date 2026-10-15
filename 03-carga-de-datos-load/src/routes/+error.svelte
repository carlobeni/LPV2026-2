<script>
  import { page } from '$app/state';
</script>

<svelte:head>
  <title>Error {page.status} — Alerta del Sistema</title>
</svelte:head>

<div class="pantalla-error">
  <div class="tarjeta-error">
    <div class="icono-alerta">⚠️</div>
    <span class="codigo-status">CÓDIGO HTTP {page.status}</span>
    
    <h1>Anomalía en la Petición</h1>
    <p class="mensaje">{page.error?.message ?? 'Se produjo un error no controlado en el servidor.'}</p>

    {#if page.error?.codigo}
      <div class="detalles-tecnicos">
        <span>Identificador Interno: <code>{page.error.codigo}</code></span>
      </div>
    {/if}

    <div class="acciones">
      <a href="/" class="btn-retorno">&larr; Retornar a la Red de Telemetría</a>
    </div>
  </div>
</div>

<style>
  .pantalla-error {
    min-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
  }

  .tarjeta-error {
    max-width: 500px;
    background: #161b22;
    border: 1px solid rgba(248, 81, 73, 0.4);
    border-radius: 12px;
    padding: 2.5rem;
    text-align: center;
  }

  .icono-alerta {
    font-size: 3rem;
    margin-bottom: 0.5rem;
  }

  .codigo-status {
    display: inline-block;
    font-size: 0.8rem;
    font-weight: 700;
    color: #ff7b72;
    background: rgba(248, 81, 73, 0.15);
    padding: 0.25rem 0.65rem;
    border-radius: 4px;
    margin-bottom: 1rem;
    letter-spacing: 0.05em;
  }

  h1 {
    font-size: 1.6rem;
    margin: 0 0 0.75rem 0;
    color: #ffffff;
  }

  .mensaje {
    color: #c9d1d9;
    font-size: 1rem;
    line-height: 1.5;
    margin-bottom: 1.5rem;
  }

  .detalles-tecnicos {
    background: #0d1117;
    border: 1px solid #30363d;
    padding: 0.75rem;
    border-radius: 6px;
    margin-bottom: 1.5rem;
    font-size: 0.85rem;
    color: #8b949e;
  }

  code {
    color: #f0883e;
    font-family: ui-monospace, monospace;
  }

  .btn-retorno {
    display: inline-block;
    background: #238636;
    color: #ffffff;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.65rem 1.25rem;
    border-radius: 6px;
    transition: background 0.2s;
  }

  .btn-retorno:hover {
    background: #2ea043;
  }
</style>
