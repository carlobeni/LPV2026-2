<script>
  // ── ESTADO DEL TEMA ───────────────────────────────────────────────────────
  let tema = $state("oscuro");       // "claro" | "oscuro"
  let hue = $state(250);             // Tono HSL del color de acento (0-360)
  let saturation = $state(70);       // Saturación HSL
  let cardActiva = $state(null);     // ID de la tarjeta activa

  // ── DATOS DE DEMO ─────────────────────────────────────────────────────────
  let tarjetas = [
    { id: 1, icono: "🤖", titulo: "Robótica",    desc: "Control y automatización de sistemas mecánicos." },
    { id: 2, icono: "⚡", titulo: "Electrónica", desc: "Diseño de circuitos y sistemas embebidos." },
    { id: 3, icono: "💻", titulo: "Software",    desc: "Programación de interfaces y APIs." },
    { id: 4, icono: "📡", titulo: "IoT",         desc: "Conectividad y sensores inteligentes." },
  ];

  // ── ESTADO DERIVADO ───────────────────────────────────────────────────────
  // Generamos el color de acento como HSL
  let colorAcento = $derived(`hsl(${hue}, ${saturation}%, 60%)`);
  let colorAcentoOscuro = $derived(`hsl(${hue}, ${saturation}%, 40%)`);
  let colorFondo = $derived(`hsl(${hue}, ${saturation}%, 8%)`);

  let esModoOscuro = $derived(tema === "oscuro");
</script>

<!-- ── TEMPLATE ──────────────────────────────────────────────────────────── -->
<!--
  Usamos custom properties CSS para pasar los valores dinámicos de Svelte al CSS.
  Esto es más eficiente que inline styles en cada elemento.
-->
<main
  class="app"
  class:modo-oscuro={esModoOscuro}
  class:modo-claro={!esModoOscuro}
  style="
    --acento: {colorAcento};
    --acento-oscuro: {colorAcentoOscuro};
    --fondo-acento: {colorFondo};
  "
>
  <header class="header">
    <div class="header-izq">
      <h1>🎨 Temas Dinámicos</h1>
      <p class="subtitulo">Sección 07 — <code>class:nombre</code>, <code>style:propiedad</code>, CSS Variables</p>
    </div>

    <!-- Toggle de tema claro/oscuro usando class: directiva -->
    <div class="controles-tema">
      <button
        class="btn-tema"
        class:activo={tema === "claro"}
        onclick={() => tema = "claro"}
      >
        ☀️ Claro
      </button>
      <button
        class="btn-tema"
        class:activo={tema === "oscuro"}
        onclick={() => tema = "oscuro"}
      >
        🌙 Oscuro
      </button>
    </div>
  </header>

  <!-- Control de color de acento -->
  <section class="panel-color">
    <h2>Color de acento</h2>
    <div class="sliders">
      <label>
        Tono (Hue): <strong style:color={colorAcento}>{hue}°</strong>
        <input type="range" bind:value={hue} min="0" max="360" class="slider-color" />
      </label>
      <label>
        Saturación: <strong>{saturation}%</strong>
        <input type="range" bind:value={saturation} min="20" max="100" />
      </label>
    </div>
    <!-- Muestra de color usando style: directiva -->
    <div class="muestra-color" style:background={colorAcento} style:color="white">
      {colorAcento}
    </div>
  </section>

  <!-- Galería de tarjetas con class: directiva para "activa" -->
  <section class="galeria">
    <h2>Tarjetas con clase dinámica</h2>
    <p class="hint-galeria">Haz click en una tarjeta para activarla.</p>

    <div class="grid">
      {#each tarjetas as tarjeta}
        <div
          class="tarjeta"
          class:activa={cardActiva === tarjeta.id}
          onclick={() => cardActiva = cardActiva === tarjeta.id ? null : tarjeta.id}
          role="button"
          tabindex="0"
          onkeydown={(e) => e.key === "Enter" && (cardActiva = tarjeta.id)}
        >
          <span class="tarjeta-icono">{tarjeta.icono}</span>
          <h3>{tarjeta.titulo}</h3>
          <p>{tarjeta.desc}</p>
          <!-- style: directiva en elementos internos -->
          <div
            class="tarjeta-barra"
            style:background={colorAcento}
            style:width={cardActiva === tarjeta.id ? "100%" : "0%"}
          ></div>
        </div>
      {/each}
    </div>

    {#if cardActiva}
      {@const t = tarjetas.find(t => t.id === cardActiva)}
      <div class="seleccion-info">
        Tarjeta activa: <strong>{t?.icono} {t?.titulo}</strong>
      </div>
    {/if}
  </section>

  <!-- Demo de class: con múltiples condiciones -->
  <section class="demo-estados">
    <h2>Demo de estados con <code>class:</code></h2>
    <div class="botones-estado">
      {#each ["exito", "advertencia", "error", "info"] as estado}
        <button
          class="estado-btn"
          class:exito={estado === "exito"}
          class:advertencia={estado === "advertencia"}
          class:error={estado === "error"}
          class:info={estado === "info"}
        >
          {{
            exito: "✓ Éxito",
            advertencia: "⚠ Advertencia",
            error: "✕ Error",
            info: "ℹ Info"
          }[estado]}
        </button>
      {/each}
    </div>
  </section>

</main>

<style>
  /* Variables CSS globales del tema → las pisa el estilo inline desde Svelte */
  :global(body) {
    margin: 0;
    font-family: 'Segoe UI', system-ui, sans-serif;
    transition: background 0.3s, color 0.3s;
  }

  /* ── TEMAS ────────────────────────────────────────────────────────────── */
  .app {
    min-height: 100vh;
    padding: 1.5rem;
    transition: background 0.3s, color 0.3s;
  }

  /* class:modo-oscuro → se aplica cuando tema === "oscuro" */
  .modo-oscuro {
    background: var(--fondo-acento, #0f0f1a);
    color: #e2e8f0;
  }

  /* class:modo-claro → se aplica cuando tema === "claro" */
  .modo-claro {
    background: #f8fafc;
    color: #1e293b;
  }

  /* ── HEADER ───────────────────────────────────────────────────────────── */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 1rem;
    max-width: 900px;
    margin: 0 auto 1.5rem;
  }

  h1 { margin: 0 0 0.2rem; font-size: 1.8rem; color: var(--acento); }
  h2 { font-size: 1rem; margin: 0 0 0.75rem; color: var(--acento); }
  .subtitulo { margin: 0; color: #64748b; font-size: 0.85rem; }

  .controles-tema {
    display: flex;
    background: rgba(128,128,128,0.1);
    border-radius: 0.6rem;
    overflow: hidden;
  }

  .btn-tema {
    padding: 0.5rem 1rem;
    border: none;
    background: transparent;
    color: inherit;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background 0.2s, color 0.2s;
  }

  /* class:activo → resalta el tema seleccionado */
  .btn-tema.activo {
    background: var(--acento);
    color: white;
    font-weight: 600;
  }

  /* ── PANEL COLOR ──────────────────────────────────────────────────────── */
  .panel-color {
    max-width: 900px;
    margin: 0 auto 1.5rem;
    background: rgba(128,128,128,0.05);
    border: 1px solid rgba(128,128,128,0.1);
    border-radius: 1rem;
    padding: 1.25rem;
  }

  .sliders {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-bottom: 0.75rem;
  }

  .sliders label {
    flex: 1;
    min-width: 200px;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
    font-size: 0.88rem;
  }

  .sliders input[type="range"] {
    accent-color: var(--acento);
  }

  .muestra-color {
    padding: 0.6rem 1rem;
    border-radius: 0.5rem;
    font-size: 0.85rem;
    font-family: monospace;
    display: inline-block;
    transition: background 0.2s;
  }

  /* ── GALERÍA ─────────────────────────────────────────────────────────── */
  .galeria {
    max-width: 900px;
    margin: 0 auto 1.5rem;
  }

  .hint-galeria { color: #64748b; font-size: 0.85rem; margin: 0 0 1rem; }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .tarjeta {
    background: rgba(128,128,128,0.05);
    border: 1px solid rgba(128,128,128,0.1);
    border-radius: 0.75rem;
    padding: 1.25rem;
    cursor: pointer;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
  }

  /* class:activa → aplica cuando cardActiva === tarjeta.id */
  .tarjeta.activa {
    border-color: var(--acento);
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--acento) 20%, transparent);
    transform: translateY(-2px);
  }

  .tarjeta:hover:not(.activa) {
    transform: translateY(-2px);
    border-color: rgba(128,128,128,0.3);
  }

  .tarjeta-icono { font-size: 2rem; display: block; margin-bottom: 0.5rem; }
  .tarjeta h3 { margin: 0 0 0.35rem; font-size: 1rem; }
  .tarjeta p { margin: 0; font-size: 0.85rem; color: #64748b; line-height: 1.5; }

  /* Barra inferior animada con style:width dinámico */
  .tarjeta-barra {
    position: absolute;
    bottom: 0; left: 0;
    height: 3px;
    transition: width 0.4s ease;
  }

  .seleccion-info {
    padding: 0.65rem 1rem;
    background: color-mix(in srgb, var(--acento) 10%, transparent);
    border: 1px solid color-mix(in srgb, var(--acento) 30%, transparent);
    border-radius: 0.5rem;
    font-size: 0.9rem;
  }

  /* ── ESTADOS ─────────────────────────────────────────────────────────── */
  .demo-estados {
    max-width: 900px;
    margin: 0 auto;
  }

  .botones-estado {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .estado-btn {
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: default;
    font-size: 0.9rem;
  }

  /* Cada clase aplica un estilo diferente */
  .estado-btn.exito      { background: #052e16; color: #4ade80; }
  .estado-btn.advertencia { background: #451a03; color: #fbbf24; }
  .estado-btn.error      { background: #450a0a; color: #f87171; }
  .estado-btn.info       { background: #0c1a2e; color: #60a5fa; }
</style>
