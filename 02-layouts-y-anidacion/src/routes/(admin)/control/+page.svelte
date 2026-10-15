<svelte:head>
  <title>Panel de Control — Layout Anidado</title>
</svelte:head>

<div class="panel-control">
  <div class="encabezado-control">
    <h2>Sala de Control y Despacho de Procesos</h2>
    <p>Esta página está anidada dentro de dos layouts simultáneamente:</p>
    <code>[+layout.svelte Raíz] &gt; [(admin)/+layout.svelte Sub-layout] &gt; control/+page.svelte</code>
  </div>

  <div class="grid-monitores">
    <div class="monitor-card">
      <span class="tag">Presión en Caldera</span>
      <div class="valor-grande">4.82 <small>bar</small></div>
      <div class="barra-progreso">
        <div class="progreso-relleno" style="width: 68%;"></div>
      </div>
      <span class="estado-ok">Rango Normal (&lt; 6.0 bar)</span>
    </div>

    <div class="monitor-card">
      <span class="tag">Temperatura Colector</span>
      <div class="valor-grande">84.5 <small>°C</small></div>
      <div class="barra-progreso">
        <div class="progreso-relleno alerta" style="width: 82%;"></div>
      </div>
      <span class="estado-alerta">Umbral de Alerta Activo</span>
    </div>
  </div>

  <div class="instruccion-didactica">
    <h4>💡 Observación Didáctica</h4>
    <p>
      Haz clic en los botones de "PARAR/ARRANCAR" de los actuadores en la barra lateral izquierda. 
      Observa cómo su estado cambia instantáneamente sin que este panel de métricas se recargue o parpadee.
    </p>
  </div>
</div>

<style>
  .panel-control {
    max-width: 900px;
  }

  .encabezado-control h2 {
    margin: 0 0 0.5rem 0;
    color: #ffffff;
    font-size: 1.6rem;
  }

  .encabezado-control p {
    color: #8b949e;
    margin: 0 0 0.75rem 0;
  }

  code {
    display: inline-block;
    background: #161b22;
    color: #58a6ff;
    padding: 0.35rem 0.6rem;
    border-radius: 6px;
    font-family: ui-monospace, monospace;
    font-size: 0.85rem;
    margin-bottom: 2rem;
  }

  .grid-monitores {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .monitor-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1.5rem;
  }

  .monitor-card .tag {
    font-size: 0.8rem;
    color: #8b949e;
    text-transform: uppercase;
  }

  .valor-grande {
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
    font-family: ui-monospace, monospace;
    margin: 0.5rem 0 1rem 0;
  }

  .valor-grande small {
    font-size: 1rem;
    color: #8b949e;
    font-weight: 400;
  }

  .barra-progreso {
    height: 6px;
    background: #21262d;
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 0.75rem;
  }

  .progreso-relleno {
    height: 100%;
    background: #238636;
  }

  .progreso-relleno.alerta {
    background: #d29922;
  }

  .estado-ok {
    font-size: 0.8rem;
    color: #3fb950;
  }

  .estado-alerta {
    font-size: 0.8rem;
    color: #d29922;
  }

  .instruccion-didactica {
    background: rgba(88, 166, 255, 0.08);
    border: 1px solid rgba(88, 166, 255, 0.2);
    border-radius: 8px;
    padding: 1.25rem;
  }

  .instruccion-didactica h4 {
    margin: 0 0 0.4rem 0;
    color: #58a6ff;
  }

  .instruccion-didactica p {
    margin: 0;
    color: #c9d1d9;
    font-size: 0.9rem;
    line-height: 1.5;
  }
</style>
