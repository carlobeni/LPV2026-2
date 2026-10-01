<script>
  // ── DATOS DEL PERFIL ──────────────────────────────────────────────────────
  // Las variables en Svelte son simplemente variables JavaScript normales.
  // En el template las interpolamos con {}.

  let nombre = "Carlos Benitez";
  let carrera = "Ingeniería Mecatrónica";
  let universidad = "FIUNA";
  let año = 3;
  let descripcion = "Apasionado por la robótica y los sistemas embebidos.";

  // Un atributo dinámico para la imagen
  let avatarSrc = `https://ui-avatars.com/api/?name=${encodeURIComponent(nombre)}&background=4f46e5&color=fff&size=128`;
  let avatarAlt = `Avatar de ${nombre}`;

  // Array de habilidades → lo usaremos en secciones siguientes con {#each}
  let habilidades = ["Python", "Svelte", "Arduino", "ROS2"];

  // HTML dinámico (ejemplo de {@html})
  let descripcionHtml = `<em>${descripcion}</em>`;
</script>

<!-- ── TEMPLATE ──────────────────────────────────────────────────────────── -->
<article class="tarjeta">

  <!-- Atributo dinámico: {src} es shorthand de src={src} -->
  <img src={avatarSrc} alt={avatarAlt} class="avatar" />

  <div class="info">
    <!-- Interpolación simple con {} -->
    <h2>{nombre}</h2>

    <!-- Expresión compuesta dentro de {} -->
    <p class="subtitulo">{carrera} · Año {año} · {universidad}</p>

    <!-- HTML dinámico con {@html} -->
    <p class="descripcion">{@html descripcionHtml}</p>

    <!-- Lista de habilidades (hardcoded por ahora; en la sección 04 usaremos {#each}) -->
    <div class="habilidades">
      {#each habilidades as habilidad}
        <span class="badge">{habilidad}</span>
      {/each}
    </div>
  </div>

</article>

<!-- ── ESTILOS SCOPED ────────────────────────────────────────────────────── -->
<style>
  /* Estos estilos SOLO afectan a TarjetaPerfil.svelte */
  .tarjeta {
    display: flex;
    gap: 1.5rem;
    align-items: center;
    background: linear-gradient(135deg, #f0f4ff, #fafaff);
    border: 1px solid #e0e7ff;
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(79, 70, 229, 0.1);
  }

  .avatar {
    width: 96px;
    height: 96px;
    border-radius: 50%;
    border: 3px solid #4f46e5;
    flex-shrink: 0;
  }

  .info {
    flex: 1;
  }

  h2 {
    margin: 0 0 0.25rem;
    font-size: 1.4rem;
    color: #1e1b4b;
  }

  .subtitulo {
    margin: 0 0 0.5rem;
    color: #6366f1;
    font-size: 0.9rem;
    font-weight: 500;
  }

  .descripcion {
    margin: 0 0 0.75rem;
    color: #4b5563;
    font-size: 0.95rem;
  }

  .habilidades {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .badge {
    background: #4f46e5;
    color: white;
    font-size: 0.75rem;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-weight: 600;
  }
</style>
