<script>
  // ── BINDINGS DEMO ─────────────────────────────────────────────────────────

  // bind:value con string
  let titulo = $state("Mi Documento Svelte");
  let contenido = $state("Escribe aquí tu contenido. Svelte actualiza la vista previa en **tiempo real**.\n\nPuede tener múltiples líneas.");

  // bind:value con number (range slider)
  let tamañoFuente = $state(16);
  let opacidad = $state(100);

  // bind:value con select
  let fuente = $state("'Segoe UI', sans-serif");
  let alineacion = $state("left");

  // bind:checked con boolean
  let mostrarBorde = $state(true);
  let modoOscuro = $state(false);

  // bind:group con array (checkboxes)
  let efectos = $state([]);

  // ── DATOS PARA SELECTS ────────────────────────────────────────────────────
  let fuentes = [
    { valor: "'Segoe UI', sans-serif",  nombre: "Segoe UI (Sans-serif)" },
    { valor: "'Georgia', serif",         nombre: "Georgia (Serif)" },
    { valor: "'Courier New', monospace", nombre: "Courier New (Mono)" },
    { valor: "'Arial', sans-serif",      nombre: "Arial" },
  ];

  // ── ESTADO DERIVADO ───────────────────────────────────────────────────────
  // Construimos el estilo del preview a partir de los bindings
  let estiloPreview = $derived([
    `font-family: ${fuente}`,
    `font-size: ${tamañoFuente}px`,
    `text-align: ${alineacion}`,
    `opacity: ${opacidad / 100}`,
    efectos.includes("negrita") ? "font-weight: bold" : "",
    efectos.includes("cursiva") ? "font-style: italic" : "",
    efectos.includes("subrayado") ? "text-decoration: underline" : "",
  ].filter(Boolean).join("; "));

  let charCount = $derived(contenido.length);
  let palabras = $derived(contenido.trim() ? contenido.trim().split(/\s+/).length : 0);
</script>

<!-- ── TEMPLATE ──────────────────────────────────────────────────────────── -->
<main class:oscuro={modoOscuro}>
  <header>
    <h1>✏️ Editor en Vivo</h1>
    <p class="subtitulo">Sección 06 — <code>bind:value</code>, <code>bind:checked</code>, <code>bind:group</code></p>
    <!-- bind:checked en el header para toggle de modo oscuro -->
    <label class="toggle-oscuro">
      <input type="checkbox" bind:checked={modoOscuro} />
      🌙 Modo oscuro
    </label>
  </header>

  <div class="layout">

    <!-- ── PANEL DE CONTROLES ─────────────────────────────────────────────── -->
    <aside class="controles">

      <!-- bind:value con string (texto) -->
      <section class="grupo">
        <h2>📝 Contenido</h2>
        <label>Título:
          <input type="text" bind:value={titulo} placeholder="Título del documento" />
        </label>
        <label>Contenido:
          <textarea rows="5" bind:value={contenido} placeholder="Escribe aquí..."></textarea>
          <span class="stats">{charCount} caracteres · {palabras} palabras</span>
        </label>
      </section>

      <!-- bind:value con number (range) -->
      <section class="grupo">
        <h2>📐 Tipografía</h2>

        <label>
          Tamaño: <strong>{tamañoFuente}px</strong>
          <input type="range" bind:value={tamañoFuente} min="10" max="36" />
        </label>

        <label>Fuente:
          <!-- bind:value con select -->
          <select bind:value={fuente}>
            {#each fuentes as f}
              <option value={f.valor}>{f.nombre}</option>
            {/each}
          </select>
        </label>

        <label>Alineación:
          <select bind:value={alineacion}>
            <option value="left">⬅ Izquierda</option>
            <option value="center">⬛ Centro</option>
            <option value="right">➡ Derecha</option>
            <option value="justify">⬜ Justificado</option>
          </select>
        </label>
      </section>

      <!-- bind:group con checkboxes (múltiples valores) -->
      <section class="grupo">
        <h2>🎨 Efectos de texto</h2>
        <div class="checkbox-grupo">
          <label>
            <input type="checkbox" bind:group={efectos} value="negrita" />
            <strong>Negrita</strong>
          </label>
          <label>
            <input type="checkbox" bind:group={efectos} value="cursiva" />
            <em>Cursiva</em>
          </label>
          <label>
            <input type="checkbox" bind:group={efectos} value="subrayado" />
            <u>Subrayado</u>
          </label>
        </div>
      </section>

      <!-- bind:value + bind:checked mezclados -->
      <section class="grupo">
        <h2>⚙️ Apariencia</h2>
        <label>
          Opacidad: <strong>{opacidad}%</strong>
          <input type="range" bind:value={opacidad} min="20" max="100" />
        </label>
        <label class="check-inline">
          <!-- bind:checked con boolean -->
          <input type="checkbox" bind:checked={mostrarBorde} />
          Mostrar borde
        </label>
      </section>

    </aside>

    <!-- ── VISTA PREVIA ───────────────────────────────────────────────────── -->
    <div class="preview" class:con-borde={mostrarBorde}>
      <div class="preview-header">Vista previa en tiempo real</div>
      <div class="preview-cuerpo" style={estiloPreview}>
        <h2>{titulo || "(sin título)"}</h2>
        <p>{contenido || "(sin contenido)"}</p>
      </div>
      <div class="preview-info">
        Estilo aplicado: <code>{estiloPreview}</code>
      </div>
    </div>

  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
    background: #f8fafc;
    color: #1e293b;
    transition: background 0.3s, color 0.3s;
  }

  main.oscuro { background: #0f172a; color: #e2e8f0; }
  main.oscuro :global(.controles) { background: #1e293b; border-color: #334155; }
  main.oscuro :global(.preview) { background: #1e293b; border-color: #334155; }
  main.oscuro :global(input), main.oscuro :global(textarea), main.oscuro :global(select) {
    background: #0f172a; border-color: #334155; color: #e2e8f0;
  }

  main { padding: 1.5rem; }

  header {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
  }

  h1 { margin: 0; font-size: 1.75rem; color: #4f46e5; }
  .subtitulo { margin: 0; color: #94a3b8; font-size: 0.85rem; flex: 1; }

  .toggle-oscuro {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    cursor: pointer;
    font-size: 0.9rem;
    color: #64748b;
  }
  .toggle-oscuro input { accent-color: #818cf8; }

  .layout {
    display: grid;
    grid-template-columns: 340px 1fr;
    gap: 1.5rem;
    align-items: start;
    max-width: 1100px;
  }

  /* Controles */
  .controles {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 1rem;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .grupo h2 {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    margin: 0 0 0.75rem;
  }

  .grupo label {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
    font-size: 0.88rem;
    margin-bottom: 0.6rem;
  }

  .grupo input[type="text"],
  .grupo textarea,
  .grupo select {
    background: #f8fafc;
    border: 1.5px solid #e2e8f0;
    border-radius: 0.4rem;
    padding: 0.5rem 0.65rem;
    font-size: 0.9rem;
    font-family: inherit;
    color: inherit;
    outline: none;
    transition: border-color 0.2s;
    resize: vertical;
  }
  .grupo input:focus, .grupo textarea:focus, .grupo select:focus {
    border-color: #818cf8;
  }

  .grupo input[type="range"] {
    accent-color: #818cf8;
    width: 100%;
  }

  .stats { font-size: 0.75rem; color: #94a3b8; text-align: right; }

  .checkbox-grupo {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }

  .checkbox-grupo label, .check-inline {
    display: flex;
    flex-direction: row !important;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
  }

  .checkbox-grupo input[type="checkbox"],
  .check-inline input[type="checkbox"] {
    accent-color: #818cf8;
    width: 16px; height: 16px;
  }

  /* Preview */
  .preview {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 1rem;
    overflow: hidden;
  }

  .preview.con-borde {
    border: 2px solid #818cf8;
    box-shadow: 0 0 0 4px rgba(129,140,248,0.1);
  }

  .preview-header {
    background: #f1f5f9;
    padding: 0.5rem 1rem;
    font-size: 0.75rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid #e2e8f0;
  }

  .preview-cuerpo {
    padding: 1.5rem;
    min-height: 200px;
    transition: all 0.2s;
    white-space: pre-wrap;
  }

  .preview-cuerpo h2 { margin: 0 0 0.75rem; font-size: 1.3em; }
  .preview-cuerpo p { margin: 0; line-height: 1.7; }

  .preview-info {
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    padding: 0.75rem 1rem;
    font-size: 0.72rem;
    color: #94a3b8;
  }

  .preview-info code {
    font-family: 'Courier New', monospace;
    word-break: break-all;
  }

  @media (max-width: 768px) {
    .layout { grid-template-columns: 1fr; }
  }
</style>
