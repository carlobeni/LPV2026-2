<script>
  // ── IMPORTACIONES DE SVELTE ───────────────────────────────────────────────
  // Svelte incluye estas funciones de transición sin necesidad de instalar nada extra
  import { fade, fly, slide, scale } from 'svelte/transition';
  import { flip } from 'svelte/animate';
  import { cubicOut, elasticOut, bounceOut } from 'svelte/easing';

  // ── ESTADO PRINCIPAL ──────────────────────────────────────────────────────
  let items = $state([
    { id: 1, texto: "Aprender Svelte básico",     completado: false, color: "#6366f1" },
    { id: 2, texto: "Entender la reactividad",    completado: false, color: "#10b981" },
    { id: 3, texto: "Dominar los bloques lógicos",completado: false, color: "#f59e0b" },
    { id: 4, texto: "Practicar eventos y bindings",completado: false, color: "#ec4899" },
    { id: 5, texto: "Aplicar transiciones",       completado: false, color: "#8b5cf6" },
  ]);

  let nuevaItem = $state("");
  let mostrarCompletados = $state(true);
  let nextId = $state(6);

  // Configuración de transición seleccionada
  let tipoTransicion = $state("fly");

  // ── ESTADO DERIVADO ───────────────────────────────────────────────────────
  let itemsVisibles = $derived(
    mostrarCompletados ? items : items.filter(i => !i.completado)
  );
  let completados = $derived(items.filter(i => i.completado).length);

  // ── COLORES PARA NUEVAS ITEMS ─────────────────────────────────────────────
  const COLORES = ["#6366f1","#10b981","#f59e0b","#ec4899","#8b5cf6","#ef4444","#06b6d4"];
  let colorIdx = $state(0);

  // ── FUNCIONES ─────────────────────────────────────────────────────────────
  function agregar() {
    if (!nuevaItem.trim()) return;
    items = [
      {
        id: nextId++,
        texto: nuevaItem.trim(),
        completado: false,
        color: COLORES[colorIdx % COLORES.length]
      },
      ...items  // Nueva item al principio → se ve la transición de entrada
    ];
    colorIdx++;
    nuevaItem = "";
  }

  function eliminar(id) {
    items = items.filter(i => i.id !== id);
  }

  function toggleCompletado(id) {
    items = items.map(i => i.id === id ? { ...i, completado: !i.completado } : i);
  }

  function mezclar() {
    // Reordenar aleatoriamente → activa animate:flip
    items = [...items].sort(() => Math.random() - 0.5);
  }

  function limpiarCompletados() {
    items = items.filter(i => !i.completado);
  }

  function manejarTecla(e) {
    if (e.key === "Enter") agregar();
  }

  // Función helper para obtener la transición correcta basada en la selección
  function getTransition(node, params) {
    const config = { duration: 400, easing: cubicOut };
    switch (tipoTransicion) {
      case "fly":   return fly(node, { ...config, x: -200 });
      case "fade":  return fade(node, config);
      case "slide": return slide(node, config);
      case "scale": return scale(node, { ...config, start: 0.5 });
      case "elastic": return fly(node, { ...config, y: -50, easing: elasticOut, duration: 600 });
      default:      return fade(node, config);
    }
  }
</script>

<!-- ── TEMPLATE ──────────────────────────────────────────────────────────── -->
<main>
  <!-- Header con fade en carga inicial (transition:fade en elemento estático) -->
  <header transition:fade={{ duration: 600 }}>
    <h1>✨ Lista Animada</h1>
    <p class="subtitulo">
      Sección 08 — <code>transition:</code>, <code>in:/out:</code>, <code>animate:flip</code>
    </p>
  </header>

  <!-- Selector de tipo de transición -->
  <section class="selector-transicion">
    <span class="label">Tipo de transición:</span>
    <div class="chips-trans">
      {#each ["fly", "fade", "slide", "scale", "elastic"] as tipo}
        <button
          class="chip"
          class:activo={tipoTransicion === tipo}
          onclick={() => tipoTransicion = tipo}
        >
          {tipo}
        </button>
      {/each}
    </div>
  </section>

  <!-- Input para agregar -->
  <div class="agregar" transition:fly={{ y: 30, duration: 400, delay: 200 }}>
    <input
      type="text"
      bind:value={nuevaItem}
      onkeydown={manejarTecla}
      placeholder="Nueva tarea... (Enter para agregar)"
    />
    <button class="btn-agregar" onclick={agregar} disabled={!nuevaItem.trim()}>+</button>
  </div>

  <!-- Controles de la lista -->
  <div class="controles">
    <span class="stats-texto">{completados}/{items.length} completadas</span>
    <div class="btns-control">
      <button onclick={mezclar} title="Mezclar (activa animate:flip)">🔀 Mezclar</button>
      <button onclick={() => mostrarCompletados = !mostrarCompletados}>
        {mostrarCompletados ? "🙈 Ocultar" : "👁️ Mostrar"} completadas
      </button>
      {#if completados > 0}
        <!-- in:fly para mostrar este botón cuando hay completadas -->
        <button
          in:fly={{ x: 50, duration: 300 }}
          out:fade={{ duration: 200 }}
          onclick={limpiarCompletados}
          class="btn-limpiar"
        >
          🗑 Limpiar ({completados})
        </button>
      {/if}
    </div>
  </div>

  <!-- Lista principal con transiciones y animate:flip -->
  <ul class="lista">
    {#each itemsVisibles as item (item.id)}
      <!--
        animate:flip: anima el movimiento cuando el orden cambia (al mezclar)
        transition: usa nuestra función getTransition según la selección del usuario
      -->
      <li
        class="item"
        class:completado={item.completado}
        style="--color-item: {item.color}"
        animate:flip={{ duration: 350, easing: cubicOut }}
        transition|global={getTransition}
      >
        <button
          class="check"
          onclick={() => toggleCompletado(item.id)}
          title={item.completado ? "Marcar pendiente" : "Marcar completado"}
        >
          {item.completado ? "✓" : ""}
        </button>

        <span class="item-texto">{item.texto}</span>

        <button class="btn-eliminar" onclick={() => eliminar(item.id)} title="Eliminar">
          ✕
        </button>
      </li>
    {:else}
      <!-- Aparece con fade cuando la lista está vacía -->
      <li class="vacio" transition:fade>
        📭 {mostrarCompletados ? "¡La lista está vacía!" : "No hay tareas pendientes 🎉"}
      </li>
    {/each}
  </ul>

  <!-- Info sobre las transiciones activas -->
  <div class="info-trans" transition:slide={{ duration: 300 }}>
    <p>
      🎬 Transición activa: <strong>{tipoTransicion}</strong> ·
      Agrega y elimina items para ver las transiciones de entrada/salida.
      Presiona <strong>🔀 Mezclar</strong> para ver <code>animate:flip</code>.
    </p>
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    background: #0a0a14;
    color: #e2e8f0;
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
    padding: 2rem 1rem;
  }

  main { max-width: 580px; margin: 0 auto; }

  header { text-align: center; margin-bottom: 1.75rem; }

  h1 {
    font-size: 2rem;
    margin: 0 0 0.25rem;
    background: linear-gradient(135deg, #818cf8, #c084fc, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .subtitulo { margin: 0; color: #475569; font-size: 0.85rem; }

  /* Selector de transición */
  .selector-transicion {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #1a1a2e;
    border: 1px solid #2d2d44;
    border-radius: 0.75rem;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
  }

  .label { font-size: 0.82rem; color: #64748b; white-space: nowrap; }

  .chips-trans { display: flex; gap: 0.4rem; flex-wrap: wrap; }

  .chip {
    padding: 0.25rem 0.75rem;
    background: #1e293b;
    border: 1px solid #334155;
    color: #94a3b8;
    border-radius: 999px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: all 0.2s;
  }

  .chip.activo {
    background: #4f46e5;
    border-color: #6366f1;
    color: white;
    font-weight: 600;
  }

  /* Input agregar */
  .agregar {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
  }

  .agregar input {
    flex: 1;
    background: #1a1a2e;
    border: 1.5px solid #2d2d44;
    color: #e2e8f0;
    padding: 0.7rem 1rem;
    border-radius: 0.65rem;
    font-size: 0.95rem;
    outline: none;
    transition: border-color 0.2s;
    font-family: inherit;
  }

  .agregar input:focus { border-color: #818cf8; }

  .btn-agregar {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    border: none;
    width: 48px;
    height: 48px;
    border-radius: 0.65rem;
    font-size: 1.5rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: opacity 0.2s;
  }

  .btn-agregar:disabled { opacity: 0.3; cursor: not-allowed; }

  /* Controles */
  .controles {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .stats-texto { font-size: 0.85rem; color: #64748b; }

  .btns-control {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
  }

  .btns-control button {
    background: #1e293b;
    border: 1px solid #334155;
    color: #94a3b8;
    padding: 0.35rem 0.7rem;
    border-radius: 0.4rem;
    cursor: pointer;
    font-size: 0.8rem;
    transition: background 0.2s, color 0.2s;
  }

  .btns-control button:hover { background: #2d3748; color: #e2e8f0; }

  .btn-limpiar { border-color: #f87171 !important; color: #f87171 !important; }
  .btn-limpiar:hover { background: #2d1016 !important; }

  /* Lista */
  .lista { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.5rem; }

  .item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #1a1a2e;
    border: 1px solid #2d2d44;
    border-left: 4px solid var(--color-item, #4f46e5);
    border-radius: 0.65rem;
    padding: 0.75rem 0.9rem;
    transition: opacity 0.3s, border-color 0.3s;
  }

  .item.completado {
    opacity: 0.45;
    border-left-color: #334155;
  }

  .item.completado .item-texto {
    text-decoration: line-through;
    color: #475569;
  }

  .check {
    width: 24px;
    height: 24px;
    border: 2px solid var(--color-item, #4f46e5);
    border-radius: 50%;
    background: transparent;
    color: var(--color-item, #4f46e5);
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 0.2s;
    flex-shrink: 0;
  }

  .item.completado .check {
    background: var(--color-item, #4f46e5);
    color: white;
    border-color: var(--color-item, #4f46e5);
  }

  .item-texto { flex: 1; font-size: 0.95rem; transition: color 0.3s; }

  .btn-eliminar {
    background: none;
    border: none;
    color: #334155;
    cursor: pointer;
    font-size: 0.8rem;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s, color 0.2s;
  }

  .btn-eliminar:hover { background: #2d1016; color: #f87171; }

  .vacio {
    text-align: center;
    color: #475569;
    padding: 2rem;
    font-style: italic;
    list-style: none;
  }

  /* Info transiciones */
  .info-trans {
    margin-top: 1.25rem;
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 0.65rem;
    padding: 0.75rem 1rem;
  }

  .info-trans p {
    margin: 0;
    font-size: 0.82rem;
    color: #475569;
    line-height: 1.6;
  }

  .info-trans strong { color: #818cf8; }
</style>
