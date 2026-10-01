<script>
  // ── ESTADO DEL FORMULARIO ─────────────────────────────────────────────────
  let nombre = $state("");
  let email = $state("");
  let asunto = $state("consulta");
  let mensaje = $state("");
  let aceptaTerminos = $state(false);

  // ── ESTADO DE UI ──────────────────────────────────────────────────────────
  let enviando = $state(false);
  let enviado = $state(false);
  let errores = $state({});
  let campoActivo = $state("");

  // ── ESTADO DERIVADO ───────────────────────────────────────────────────────
  let charsMensaje = $derived(mensaje.length);
  let maxChars = 300;
  let formularioValido = $derived(
    nombre.trim().length >= 2 &&
    email.includes("@") &&
    mensaje.trim().length >= 10 &&
    aceptaTerminos
  );

  // ── FUNCIONES DE VALIDACIÓN ───────────────────────────────────────────────
  function validarCampo(campo) {
    let nuevoErrores = { ...errores };

    if (campo === "nombre") {
      nuevoErrores.nombre = nombre.trim().length < 2
        ? "El nombre debe tener al menos 2 caracteres." : "";
    }
    if (campo === "email") {
      nuevoErrores.email = !email.includes("@") || !email.includes(".")
        ? "Ingresa un email válido (ej: usuario@dominio.com)." : "";
    }
    if (campo === "mensaje") {
      nuevoErrores.mensaje = mensaje.trim().length < 10
        ? "El mensaje debe tener al menos 10 caracteres." : "";
    }

    errores = nuevoErrores;
  }

  // ── MANEJADORES DE EVENTOS ────────────────────────────────────────────────

  // onblur: valida cuando el usuario abandona el campo
  function alPerderFoco(campo) {
    campoActivo = "";
    validarCampo(campo);
  }

  // onfocus: registra qué campo está activo
  function alEnfocar(campo) {
    campoActivo = campo;
  }

  // onkeydown: detecta teclas especiales
  function alPrecionar(e) {
    if (e.key === "Escape") {
      // Deselecciona el campo activo
      e.target.blur();
    }
  }

  // onsubmit: maneja el envío del formulario
  async function manejarSubmit(e) {
    e.preventDefault();  // ← Evita el comportamiento por defecto del formulario

    // Validar todos los campos
    ["nombre", "email", "mensaje"].forEach(validarCampo);

    if (!formularioValido) return;

    enviando = true;

    // Simulamos una petición de red (fetch a API)
    await new Promise(r => setTimeout(r, 1800));

    enviando = false;
    enviado = true;
  }

  function reiniciar() {
    nombre = email = mensaje = "";
    asunto = "consulta";
    aceptaTerminos = false;
    errores = {};
    enviado = false;
  }
</script>

<!-- ── TEMPLATE ──────────────────────────────────────────────────────────── -->
<main>
  <div class="contenedor">

    {#if enviado}
      <!-- Estado: formulario enviado exitosamente -->
      <div class="exito">
        <div class="exito-icono">✓</div>
        <h2>¡Mensaje enviado!</h2>
        <p>Gracias, <strong>{nombre}</strong>. Te contactaremos en {email} a la brevedad.</p>
        <button class="btn-primario" onclick={reiniciar}>Enviar otro mensaje</button>
      </div>

    {:else}
      <!-- Estado: formulario normal -->
      <header>
        <h1>📬 Formulario de Contacto</h1>
        <p class="subtitulo">Sección 05 — Eventos: <code>onsubmit</code>, <code>oninput</code>, <code>onblur</code>, <code>onfocus</code></p>
      </header>

      <!-- El evento onsubmit llama a manejarSubmit y preventDefault() evita recarga -->
      <form onsubmit={manejarSubmit} novalidate>

        <!-- Campo: Nombre -->
        <div class="campo" class:activo={campoActivo === "nombre"} class:error={errores.nombre}>
          <label for="nombre">Nombre completo *</label>
          <input
            id="nombre"
            type="text"
            bind:value={nombre}
            placeholder="Ej: Carlos Benitez"
            onfocus={() => alEnfocar("nombre")}
            onblur={() => alPerderFoco("nombre")}
            onkeydown={alPrecionar}
          />
          {#if errores.nombre}
            <span class="error-msg">{errores.nombre}</span>
          {/if}
        </div>

        <!-- Campo: Email -->
        <div class="campo" class:activo={campoActivo === "email"} class:error={errores.email}>
          <label for="email">Email *</label>
          <input
            id="email"
            type="email"
            bind:value={email}
            placeholder="usuario@ejemplo.com"
            onfocus={() => alEnfocar("email")}
            onblur={() => alPerderFoco("email")}
          />
          {#if errores.email}
            <span class="error-msg">{errores.email}</span>
          {/if}
        </div>

        <!-- Campo: Asunto (onchange para select) -->
        <div class="campo">
          <label for="asunto">Asunto</label>
          <select id="asunto" bind:value={asunto} onchange={() => console.log("Asunto:", asunto)}>
            <option value="consulta">Consulta general</option>
            <option value="soporte">Soporte técnico</option>
            <option value="proyecto">Propuesta de proyecto</option>
            <option value="otro">Otro</option>
          </select>
        </div>

        <!-- Campo: Mensaje (con contador de caracteres via oninput) -->
        <div class="campo" class:activo={campoActivo === "mensaje"} class:error={errores.mensaje}>
          <label for="mensaje">
            Mensaje *
            <!-- Evento oninput: actualiza el estado en cada tecla -->
            <span class="chars" class:limite={charsMensaje > maxChars * 0.9}>
              {charsMensaje}/{maxChars}
            </span>
          </label>
          <textarea
            id="mensaje"
            rows="4"
            bind:value={mensaje}
            placeholder="Cuéntanos en qué podemos ayudarte..."
            maxlength={maxChars}
            onfocus={() => alEnfocar("mensaje")}
            onblur={() => alPerderFoco("mensaje")}
          ></textarea>
          {#if errores.mensaje}
            <span class="error-msg">{errores.mensaje}</span>
          {/if}
        </div>

        <!-- Checkbox con onchange -->
        <div class="campo-check">
          <input
            id="terminos"
            type="checkbox"
            bind:checked={aceptaTerminos}
            onchange={() => console.log("Términos aceptados:", aceptaTerminos)}
          />
          <label for="terminos">
            Acepto los <a href="#terminos">términos y condiciones</a>
          </label>
        </div>

        <!-- Botón de envío -->
        <button
          type="submit"
          class="btn-primario"
          disabled={!formularioValido || enviando}
        >
          {#if enviando}
            <span class="spinner"></span> Enviando...
          {:else}
            ✉ Enviar mensaje
          {/if}
        </button>

        <!-- Indicador de campos requeridos -->
        {#if !formularioValido}
          <p class="hint">* Completa todos los campos requeridos para enviar.</p>
        {/if}

      </form>
    {/if}
  </div>
</main>

<!-- ── ESTILOS ────────────────────────────────────────────────────────────── -->
<style>
  :global(body) {
    margin: 0;
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
    color: #e2e8f0;
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 2rem 1rem;
  }

  main { width: 100%; }

  .contenedor {
    max-width: 520px;
    margin: 0 auto;
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 1.25rem;
    padding: 2rem;
  }

  h1 { font-size: 1.75rem; margin: 0 0 0.25rem; color: #f1f5f9; }
  .subtitulo { color: #475569; font-size: 0.85rem; margin: 0 0 1.75rem; }

  /* Campos */
  .campo {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    margin-bottom: 1rem;
  }

  .campo label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
  }

  .campo input,
  .campo textarea,
  .campo select {
    background: #0f172a;
    border: 1.5px solid #334155;
    color: #e2e8f0;
    padding: 0.65rem 0.9rem;
    border-radius: 0.5rem;
    font-size: 0.95rem;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
    font-family: inherit;
    resize: vertical;
  }

  .campo.activo input,
  .campo.activo textarea,
  .campo.activo select {
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
  }

  .campo.error input,
  .campo.error textarea {
    border-color: #ef4444;
    box-shadow: 0 0 0 3px rgba(239,68,68,0.1);
  }

  .error-msg {
    font-size: 0.78rem;
    color: #f87171;
    margin-top: 0.1rem;
  }

  .chars {
    font-size: 0.75rem;
    color: #475569;
    font-weight: 400;
  }
  .chars.limite { color: #f59e0b; }

  /* Checkbox */
  .campo-check {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.25rem;
    font-size: 0.9rem;
    color: #94a3b8;
  }
  .campo-check input { accent-color: #6366f1; width: 16px; height: 16px; }
  .campo-check a { color: #818cf8; text-decoration: none; }

  /* Botón */
  .btn-primario {
    width: 100%;
    padding: 0.85rem;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    border: none;
    border-radius: 0.65rem;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    transition: opacity 0.2s, transform 0.1s;
  }
  .btn-primario:disabled { opacity: 0.4; cursor: not-allowed; }
  .btn-primario:not(:disabled):hover { opacity: 0.9; }
  .btn-primario:not(:disabled):active { transform: scale(0.98); }

  .spinner {
    width: 16px; height: 16px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .hint {
    text-align: center;
    color: #475569;
    font-size: 0.8rem;
    margin: 0.75rem 0 0;
  }

  /* Estado éxito */
  .exito {
    text-align: center;
    padding: 2rem 1rem;
  }
  .exito-icono {
    width: 72px; height: 72px;
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    font-size: 2rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
  }
  .exito h2 { color: #4ade80; margin: 0 0 0.5rem; }
  .exito p { color: #94a3b8; margin: 0 0 1.5rem; }
</style>
