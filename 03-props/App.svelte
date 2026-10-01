<script>
  import TarjetaProyecto from './TarjetaProyecto.svelte';

  // Array de proyectos — en la sección 04 aprenderemos a iterar sobre estos con {#each}
  let proyectos = $state([
    {
      titulo: "Robot Seguidor de Línea",
      descripcion: "Vehículo autónomo que sigue una trayectoria usando sensores IR y controlador PID.",
      tecnologias: ["Arduino", "C++", "PID"],
      color: "#10b981",
      completado: true
    },
    {
      titulo: "Brazo Robótico 6 DOF",
      descripcion: "Brazo manipulador con 6 grados de libertad controlado mediante cinemática inversa.",
      tecnologias: ["Python", "ROS2", "MoveIt"],
      color: "#6366f1",
      completado: false
    },
    {
      titulo: "Dashboard IoT con Svelte",
      descripcion: "Panel de monitoreo en tiempo real para sensores industriales via MQTT.",
      tecnologias: ["Svelte", "MQTT", "Node.js"],
      color: "#f59e0b",
      completado: true
    },
    {
      titulo: "Control de Velocidad VFD",
      descripcion: "Sistema de control de frecuencia variable para motores trifásicos con HMI.",
      tecnologias: ["Modbus", "Python", "Tkinter"],
      color: "#ec4899",
      completado: false
    }
  ]);
</script>

<main>
  <h1>🚀 Mis Proyectos</h1>
  <p class="subtitulo">Sección 03 — Props: cada tarjeta recibe datos como <code>props</code></p>

  <div class="galeria">
    {#each proyectos as proyecto}
      <!-- Spread props: equivale a pasar cada propiedad individualmente -->
      <TarjetaProyecto {...proyecto} />
    {/each}
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    background: #0a0a0f;
    color: #e2e8f0;
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
    padding: 2rem 1rem;
  }

  main {
    max-width: 900px;
    margin: 0 auto;
  }

  h1 {
    font-size: 2rem;
    margin: 0 0 0.5rem;
    background: linear-gradient(135deg, #f59e0b, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .subtitulo {
    color: #475569;
    margin: 0 0 2rem;
  }

  .galeria {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.25rem;
  }
</style>
