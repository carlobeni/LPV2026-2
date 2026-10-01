<script>
  // ── ESTADO PRINCIPAL ──────────────────────────────────────────────────────
  let tareas = $state([
    { id: 1, texto: "Leer la documentación de Svelte", completada: true,  prioridad: "alta" },
    { id: 2, texto: "Crear el primer componente",      completada: true,  prioridad: "alta" },
    { id: 3, texto: "Aprender $state y $derived",      completada: false, prioridad: "alta" },
    { id: 4, texto: "Practicar {#each} y {#if}",       completada: false, prioridad: "media" },
    { id: 5, texto: "Construir la mini página",        completada: false, prioridad: "media" },
    { id: 6, texto: "Completar los ejercicios",        completada: false, prioridad: "baja"  },
  ]);

  let nuevaTarea = $state("");
  let filtro = $state("todas"); // "todas" | "pendientes" | "completadas"
  let nextId = $state(7);

  // ── ESTADO DERIVADO ───────────────────────────────────────────────────────
  // {#each} iterará sobre esta lista filtrada
  let tareasFiltradas = $derived(
    filtro === "completadas" ? tareas.filter(t => t.completada)
    : filtro === "pendientes" ? tareas.filter(t => !t.completada)
    : tareas
  );

  let totalCompletadas = $derived(tareas.filter(t => t.completada).length);
  let progreso = $derived(tareas.length ? Math.round((totalCompletadas / tareas.length) * 100) : 0);

  // ── PROMESA (para demostrar {#await}) ────────────────────────────────────
  async function cargarCita() {
    await new Promise(r => setTimeout(r, 1200)); // Simula latencia de red
    const frases = [
      "La constancia es el camino al éxito.",
      "Cada línea de código es un paso adelante.",
      "Svelte hace que programar sea divertido.",
      "La práctica diaria supera al talento innato."
    ];
    return frases[Math.floor(Math.random() * frases.length)];
  }

  let promesaCita = $state(cargarCita());

  // ── FUNCIONES ─────────────────────────────────────────────────────────────
  function agregar() {
    if (!nuevaTarea.trim()) return;
    tareas = [...tareas, {
      id: nextId++,
      texto: nuevaTarea.trim(),
      completada: false,
      prioridad: "media"
    }];
    nuevaTarea = "";
  }

  function toggleTarea(id) {
    tareas = tareas.map(t => t.id === id ? { ...t, completada: !t.completada } : t);
  }

  function eliminar(id) {
    tareas = tareas.filter(t => t.id !== id);
  }

  function recargarCita() {
    promesaCita = cargarCita();
  }

  // Manejar Enter en el input
  function manejarTecla(e) {
    if (e.key === "Enter") agregar();
  }
</script>

<!-- ── TEMPLATE ──────────────────────────────────────────────────────────── -->
<main>
  <header>
    <h1>📋 Dashboard de Tareas</h1>
    <p class="subtitulo">Sección 04 — <code>{"{#if}"}</code>, <code>{"{#each}"}</code>, <code>{"{#await}"}</code></p>
  </header>

  <!-- SECCIÓN {#await}: Cita motivacional cargada asincrónicamente -->
  <section class="cita-box">
    <span class="cita-label">💡 Cita del día ({"{#await}"}):</span>
    {#await promesaCita}
      <span class="cita-cargando">Cargando cita...</span>
    {:then cita}
      <span class="cita-texto">"{cita}"</span>
    {:catch error}
      <span class="cita-error">Error: {error.message}</span>
    {/await}
    <button class="btn-reload" onclick={recargarCita}>↻</button>
  </section>

  <!-- Barra de progreso -->
  <section class="progreso">
    <div class="progreso-info">
      <span>{totalCompletadas} de {tareas.length} completadas</span>
      <span class="pct">{progreso}%</span>
    </div>
    <div class="barra">
      <div class="barra-relleno" style="width: {progreso}%"></div>
    </div>
  </section>

  <!-- Input para agregar tarea -->
  <div class="agregar">
    <input
      type="text"
      placeholder="Nueva tarea..."
      bind:value={nuevaTarea}
      onkeydown={manejarTecla}
    />
    <button onclick={agregar} disabled={!nuevaTarea.trim()}>+ Agregar</button>
  </div>

  <!-- Filtros ({#if} para resaltar el activo) -->
  <div class="filtros">
    {#each ["todas", "pendientes", "completadas"] as opcion}
      <button
        class="filtro-btn"
        class:activo={filtro === opcion}
        onclick={() => filtro = opcion}
      >
        {opcion}
      </button>
    {/each}
  </div>

  <!-- Lista de tareas ({#each} principal) -->
  <ul class="lista">
    {#each tareasFiltradas as tarea (tarea.id)}

      <li class="tarea-item" class:completada={tarea.completada}>
        <input
          type="checkbox"
          checked={tarea.completada}
          onchange={() => toggleTarea(tarea.id)}
          id="tarea-{tarea.id}"
        />
        <label for="tarea-{tarea.id}">{tarea.texto}</label>

        <!-- {#if} para mostrar condicionalmente la prioridad -->
        {#if tarea.prioridad === "alta"}
          <span class="prioridad alta">🔴</span>
        {:else if tarea.prioridad === "media"}
          <span class="prioridad media">🟡</span>
        {:else}
          <span class="prioridad baja">🟢</span>
        {/if}

        <button class="btn-eliminar" onclick={() => eliminar(tarea.id)} title="Eliminar">✕</button>
      </li>

    {:else}
      <!-- {/each} con {:else}: se muestra cuando la lista está vacía -->
      <li class="vacio">
        {#if filtro === "completadas"}
          ✓ No hay tareas completadas aún.
        {:else if filtro === "pendientes"}
          🎉 ¡No hay tareas pendientes!
        {:else}
          📭 Agrega tu primera tarea arriba.
        {/if}
      </li>
    {/each}
  </ul>
</main>

<!-- ── ESTILOS ────────────────────────────────────────────────────────────── -->
<style>
  :global(body) {
    margin: 0;
    background: #0d1117;
    color: #c9d1d9;
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
    padding: 2rem 1rem;
  }

  main {
    max-width: 560px;
    margin: 0 auto;
  }

  h1 {
    font-size: 1.8rem;
    margin: 0 0 0.25rem;
    color: #f0f6fc;
  }

  .subtitulo {
    color: #484f58;
    margin: 0 0 1.5rem;
    font-size: 0.9rem;
  }

  /* Cita motivacional */
  .cita-box {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 0.75rem;
    padding: 0.75rem 1rem;
    margin-bottom: 1.25rem;
    font-size: 0.9rem;
  }

  .cita-label { color: #484f58; white-space: nowrap; font-size: 0.8rem; }
  .cita-texto { color: #8b949e; flex: 1; font-style: italic; }
  .cita-cargando { color: #58a6ff; flex: 1; animation: pulse 1s infinite alternate; }
  .cita-error { color: #f85149; flex: 1; }

  @keyframes pulse { from { opacity: 0.5; } to { opacity: 1; } }

  .btn-reload {
    background: none;
    border: 1px solid #30363d;
    color: #8b949e;
    border-radius: 50%;
    width: 28px; height: 28px;
    cursor: pointer;
    font-size: 1rem;
    display: flex; align-items: center; justify-content: center;
    transition: background 0.2s, color 0.2s;
  }
  .btn-reload:hover { background: #21262d; color: #58a6ff; }

  /* Progreso */
  .progreso {
    margin-bottom: 1.25rem;
  }
  .progreso-info {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    color: #8b949e;
    margin-bottom: 0.35rem;
  }
  .pct { font-weight: 700; color: #58a6ff; }
  .barra {
    background: #21262d;
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
  }
  .barra-relleno {
    height: 100%;
    background: linear-gradient(90deg, #238636, #4ade80);
    border-radius: 999px;
    transition: width 0.4s ease;
  }

  /* Input agregar */
  .agregar {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
  }
  .agregar input {
    flex: 1;
    background: #161b22;
    border: 1px solid #30363d;
    color: #c9d1d9;
    padding: 0.6rem 0.9rem;
    border-radius: 0.5rem;
    font-size: 0.95rem;
    outline: none;
    transition: border-color 0.2s;
  }
  .agregar input:focus { border-color: #58a6ff; }
  .agregar button {
    background: #238636;
    color: white;
    border: none;
    padding: 0.6rem 1rem;
    border-radius: 0.5rem;
    cursor: pointer;
    font-weight: 600;
    transition: background 0.2s;
  }
  .agregar button:disabled { background: #21262d; color: #484f58; cursor: not-allowed; }
  .agregar button:not(:disabled):hover { background: #2ea043; }

  /* Filtros */
  .filtros {
    display: flex;
    gap: 0.4rem;
    margin-bottom: 1rem;
  }
  .filtro-btn {
    flex: 1;
    padding: 0.4rem;
    background: #161b22;
    border: 1px solid #30363d;
    color: #8b949e;
    border-radius: 0.5rem;
    cursor: pointer;
    font-size: 0.8rem;
    text-transform: capitalize;
    transition: all 0.2s;
  }
  .filtro-btn.activo {
    background: #1f6feb;
    border-color: #388bfd;
    color: white;
    font-weight: 600;
  }

  /* Lista */
  .lista {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }

  .tarea-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 0.5rem;
    padding: 0.65rem 0.9rem;
    transition: opacity 0.2s;
  }

  .tarea-item.completada {
    opacity: 0.5;
  }

  .tarea-item input[type="checkbox"] {
    accent-color: #4ade80;
    width: 16px; height: 16px;
    cursor: pointer;
    flex-shrink: 0;
  }

  .tarea-item label {
    flex: 1;
    cursor: pointer;
    font-size: 0.95rem;
  }

  .tarea-item.completada label {
    text-decoration: line-through;
  }

  .prioridad { font-size: 0.8rem; }

  .btn-eliminar {
    background: none;
    border: none;
    color: #484f58;
    cursor: pointer;
    font-size: 0.85rem;
    padding: 0.2rem;
    border-radius: 0.25rem;
    transition: color 0.2s, background 0.2s;
  }
  .btn-eliminar:hover { color: #f85149; background: #2d1016; }

  .vacio {
    text-align: center;
    color: #484f58;
    padding: 2rem;
    font-style: italic;
  }
</style>
