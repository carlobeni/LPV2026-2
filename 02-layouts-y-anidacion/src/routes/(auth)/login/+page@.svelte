<script>
  let usuario = $state('operador1');
  let password = $state('');
  let mensaje = $state('');

  function iniciarSesion(e) {
    e.preventDefault();
    mensaje = `Autenticando operario: ${usuario}...`;
  }
</script>

<svelte:head>
  <title>Acceso Seguro — Layout Reseteado (@)</title>
</svelte:head>

<div class="pantalla-completa-login">
  <div class="tarjeta-login">
    <div class="aviso-layout">
      <span>Layout Reseteado: <code>+page@.svelte</code></span>
    </div>

    <h2>Acceso al Sistema SCADA</h2>
    <p class="sub">Autenticación de Operadores Mecatrónicos</p>

    <form onsubmit={iniciarSesion}>
      <div class="campo">
        <label for="u">Código de Operario / ID:</label>
        <input id="u" type="text" bind:value={usuario} required />
      </div>

      <div class="campo">
        <label for="p">Clave de Seguridad:</label>
        <input id="p" type="password" bind:value={password} placeholder="••••••••" required />
      </div>

      <button type="submit" class="btn-entrar">Ingresar al Sistema</button>
    </form>

    {#if mensaje}
      <p class="status-msg">{mensaje}</p>
    {/if}

    <div class="footer-login">
      <a href="/">&larr; Volver a la aplicación con layout normal</a>
    </div>
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    background: #090d13;
    font-family: system-ui, sans-serif;
  }

  .pantalla-completa-login {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
    background: radial-gradient(circle at center, #161b22 0%, #090d13 100%);
  }

  .tarjeta-login {
    width: 100%;
    max-width: 400px;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 2.25rem;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5);
  }

  .aviso-layout {
    margin-bottom: 1.25rem;
  }

  .aviso-layout span {
    display: inline-block;
    font-size: 0.75rem;
    background: #d29922;
    color: #0d1117;
    font-weight: 700;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
  }

  h2 {
    margin: 0 0 0.35rem 0;
    color: #ffffff;
    font-size: 1.5rem;
  }

  .sub {
    color: #8b949e;
    font-size: 0.85rem;
    margin: 0 0 1.5rem 0;
  }

  .campo {
    margin-bottom: 1.25rem;
  }

  label {
    display: block;
    font-size: 0.8rem;
    color: #8b949e;
    margin-bottom: 0.4rem;
  }

  input {
    width: 100%;
    box-sizing: border-box;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #e6edf3;
    padding: 0.65rem 0.85rem;
    font-size: 0.95rem;
    outline: none;
  }

  input:focus {
    border-color: #58a6ff;
  }

  .btn-entrar {
    width: 100%;
    background: #238636;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 0.75rem;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    margin-top: 0.5rem;
    transition: background 0.2s;
  }

  .btn-entrar:hover {
    background: #2ea043;
  }

  .status-msg {
    margin-top: 1rem;
    font-size: 0.85rem;
    color: #3fb950;
    text-align: center;
  }

  .footer-login {
    margin-top: 1.5rem;
    border-top: 1px solid #21262d;
    padding-top: 1.25rem;
    text-align: center;
  }

  .footer-login a {
    color: #58a6ff;
    font-size: 0.85rem;
    text-decoration: none;
  }

  .footer-login a:hover {
    text-decoration: underline;
  }
</style>
