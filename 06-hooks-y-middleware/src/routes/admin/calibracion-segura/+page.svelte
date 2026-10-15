<script>
  let { data } = $props();
</script>

<svelte:head>
  <title>Zona Protegida — Calibración Segura</title>
</svelte:head>

<div class="contenedor">
  <div class="zona-segura">
    <div class="header-zona">
      <span class="badge-seguridad">🛡️ ZONA RESTRINGIDA RBAC</span>
      <h1>Calibración de Parámetros Críticos de Planta</h1>
      <p>
        Acceso concedido satisfactoriamente a: <strong>{data.usuario?.nombre}</strong> 
        (Rol verificado: <code>{data.usuario?.rol}</code>)
      </p>
    </div>

    <div class="panel-peligro">
      <h3>⚠️ Advertencia de Seguridad Operativa</h3>
      <p>
        Cualquier modificación efectuada en este panel alterará las constantes PID de los lazos de control de lazo cerrado en los controladores industriales.
      </p>
    </div>

    <div class="grid-parametros">
      <div class="param">
        <label for="p1">Ganancia Proporcional (Kp):</label>
        <input id="p1" type="number" value="2.45" step="0.05" />
      </div>
      <div class="param">
        <label for="p2">Tiempo Integral (Ti - seg):</label>
        <input id="p2" type="number" value="18.2" step="0.1" />
      </div>
      <div class="param">
        <label for="p3">Tiempo Derivativo (Td - seg):</label>
        <input id="p3" type="number" value="1.15" step="0.05" />
      </div>
    </div>

    <div class="acciones-admin">
      <a href="/" class="btn-volver">&larr; Retornar al Menú Principal</a>
      <button class="btn-guardar" onclick={() => alert('Parámetros PID actualizados en el PLC.')}>
        Aplicar en Bus CAN
      </button>
    </div>
  </div>
</div>

<style>
  .contenedor {
    max-width: 800px;
    margin: 3rem auto;
    padding: 0 1.5rem;
  }

  .zona-segura {
    background: #161b22;
    border: 1px solid #8957e5;
    border-radius: 12px;
    padding: 2.25rem;
  }

  .badge-seguridad {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    color: #d2a8ff;
    background: rgba(137, 87, 229, 0.2);
    border: 1px solid rgba(137, 87, 229, 0.4);
    padding: 0.25rem 0.65rem;
    border-radius: 4px;
    margin-bottom: 0.75rem;
  }

  h1 {
    font-size: 1.8rem;
    margin: 0 0 0.5rem 0;
    color: #ffffff;
  }

  p {
    color: #8b949e;
    margin: 0 0 1.5rem 0;
  }

  code {
    color: #58a6ff;
  }

  .panel-peligro {
    background: rgba(210, 153, 34, 0.12);
    border-left: 4px solid #d29922;
    padding: 1rem 1.25rem;
    border-radius: 0 8px 8px 0;
    margin-bottom: 1.75rem;
  }

  .panel-peligro h3 {
    margin: 0 0 0.35rem 0;
    font-size: 1rem;
    color: #e3b341;
  }

  .panel-peligro p {
    margin: 0;
    color: #c9d1d9;
    font-size: 0.85rem;
  }

  .grid-parametros {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.25rem;
    margin-bottom: 2rem;
  }

  .param label {
    display: block;
    font-size: 0.8rem;
    color: #8b949e;
    margin-bottom: 0.4rem;
  }

  .param input {
    width: 100%;
    box-sizing: border-box;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #e6edf3;
    padding: 0.6rem 0.75rem;
    font-size: 0.95rem;
    font-family: ui-monospace, monospace;
  }

  .acciones-admin {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #21262d;
    padding-top: 1.5rem;
  }

  .btn-volver {
    color: #58a6ff;
    text-decoration: none;
    font-size: 0.9rem;
  }

  .btn-volver:hover {
    text-decoration: underline;
  }

  .btn-guardar {
    background: #238636;
    color: #ffffff;
    border: none;
    padding: 0.65rem 1.25rem;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
  }

  .btn-guardar:hover {
    background: #2ea043;
  }
</style>
