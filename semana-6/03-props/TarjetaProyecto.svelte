<script>
  // ── PROPS ─────────────────────────────────────────────────────────────────
  // $props() es la rune para declarar props en Svelte 5.
  // Usamos desestructuración con valores por defecto.

  let {
    titulo = "Sin título",
    descripcion = "Sin descripción disponible.",
    tecnologias = [],        // Array de strings
    color = "#4f46e5",       // Color del acento
    completado = false       // Booleano
  } = $props();
</script>

<!-- ── TEMPLATE ──────────────────────────────────────────────────────────── -->
<article class="tarjeta" style="--color-acento: {color}">

  <!-- Indicador de estado -->
  <div class="estado" class:completado>
    {completado ? "✓ Completado" : "⏳ En progreso"}
  </div>

  <h2>{titulo}</h2>
  <p>{descripcion}</p>

  <!-- Lista de tecnologías (recibida como prop array) -->
  <div class="tecnologias">
    {#each tecnologias as tech}
      <span class="tag">{tech}</span>
    {/each}
  </div>

</article>

<style>
  .tarjeta {
    background: #1a1a2e;
    border: 1px solid #2d2d44;
    border-left: 4px solid var(--color-acento);
    border-radius: 0.75rem;
    padding: 1.25rem;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
  }

  .tarjeta::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, var(--color-acento), transparent);
    opacity: 0.5;
  }

  .tarjeta:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
  }

  .estado {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    margin-bottom: 0.75rem;
    background: #1e3a5f;
    color: #60a5fa;
  }

  .estado.completado {
    background: #052e16;
    color: #4ade80;
  }

  h2 {
    margin: 0 0 0.5rem;
    font-size: 1.1rem;
    color: var(--color-acento);
  }

  p {
    color: #94a3b8;
    font-size: 0.9rem;
    line-height: 1.6;
    margin: 0 0 1rem;
  }

  .tecnologias {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .tag {
    font-size: 0.75rem;
    background: #0f172a;
    color: #94a3b8;
    border: 1px solid #334155;
    padding: 0.15rem 0.5rem;
    border-radius: 0.25rem;
    font-family: 'Courier New', monospace;
  }
</style>
