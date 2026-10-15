<svelte:head>
  <title>Arquitectura del Sistema — SCADA SvelteKit 2</title>
</svelte:head>

<div class="contenedor-about">
  <div class="tarjeta-documento">
    <div class="doc-header">
      <span class="badge-doc">ESPECIFICACIÓN DE INGENIERÍA</span>
      <h1>Arquitectura de la Plataforma SCADA Full-Stack</h1>
      <p class="sub">Integración de SvelteKit 2, Svelte 5 (Runes) y Telecomunicaciones en Tiempo Real</p>
    </div>

    <div class="seccion-bloque">
      <h3>1. Diagrama de Flujo de Datos y Capas</h3>
      <div class="diagrama-ascii">
        <pre><code>
┌────────────────────────────────────────────────────────┐
│                   NAVEGADOR (CLIENTE)                  │
│                                                        │
│   +page.svelte (Runes $state, $derived, $effect)       │
│     ├── EventSource('/api/telemetria/stream') (1 Hz)  │
│     ├── Osciloscopio SVG Reactivo                      │
│     └── use:enhance (Mutaciones Form Actions sin recarga│
└───────────────────────▲───────────────▲────────────────┘
                        │               │
                 SSE (Stream)      Form Actions (POST)
                        │               │
┌───────────────────────┴───────────────┴────────────────┐
│                 SERVIDOR SVELTEKIT 2                   │
│                                                        │
│   src/hooks.server.js (Middleware Global)             │
│     ├── Verificación de Sesión y Roles (RBAC)         │
│     └── Inyección de Server-Timing Header              │
│                                                        │
│   Rutas de Servidor:                                   │
│     ├── +page.server.js (load inicial & actions)       │
│     ├── /api/telemetria/stream/+server.js (SSE)       │
│     └── /api/exportar/+server.js (Streaming CSV)       │
└────────────────────────────────────────────────────────┘
        </code></pre>
      </div>
    </div>

    <div class="seccion-bloque">
      <h3>2. Tecnologías y Patrones Aplicados</h3>
      <table class="tabla-specs">
        <thead>
          <tr>
            <th>Capa</th>
            <th>Tecnología / Mecanismo</th>
            <th>Justificación Mecatrónica</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Revisión de Seguridad</strong></td>
            <td><code>src/hooks.server.js</code></td>
            <td>Garantiza que sólo personal calificado (Ingeniero Jefe) active comandos críticos antes de que lleguen a la lógica de la planta.</td>
          </tr>
          <tr>
            <td><strong>Telemetría en Vivo</strong></td>
            <td><code>Server-Sent Events (SSE)</code></td>
            <td>Protocolo unidireccional HTTP liviano, compatible con proxies y cortafuegos industriales sin el overhead de WebSockets.</td>
          </tr>
          <tr>
            <td><strong>Mutaciones de Planta</strong></td>
            <td><code>Form Actions + use:enhance</code></td>
            <td>Proporciona soporte nativo accesible e inmediato con rollback y validación tipada en servidor.</td>
          </tr>
          <tr>
            <td><strong>Visualización Gráfica</strong></td>
            <td><code>SVG Puro con Runes ($derived)</code></td>
            <td>Cero dependencias externas (Canvas/Chart.js), renderizado vectorial ultrarrápido y control milimétrico del DOM.</td>
          </tr>
          <tr>
            <td><strong>Exportación Legal</strong></td>
            <td><code>Streaming HTTP Response CSV</code></td>
            <td>Generación al vuelo de registros de auditoría sin consumir memoria en disco del servidor.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="seccion-bloque">
      <h3>3. Cómo Ejecutar Este Proyecto Localmente</h3>
      <div class="codigo-box">
        <pre><code># 1. Ingresar al directorio del proyecto avanzado
cd 07-proyecto-avanzado-dashboard

# 2. Instalar dependencias (si no se han instalado)
npm install

# 3. Iniciar el servidor de desarrollo Vite
npm run dev

# 4. Abrir en el navegador:
# http://localhost:5173</code></pre>
      </div>
    </div>
  </div>
</div>

<style>
  .contenedor-about {
    max-width: 950px;
    margin: 2.5rem auto;
    padding: 0 1.5rem;
  }

  .tarjeta-documento {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 2.5rem;
  }

  .doc-header {
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
  }

  .badge-doc {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--color-accent);
    letter-spacing: 0.08em;
  }

  h1 {
    font-size: 1.85rem;
    margin: 0.5rem 0 0.5rem 0;
    color: var(--text-primary);
  }

  .sub {
    color: var(--text-secondary);
    margin: 0;
    font-size: 0.95rem;
  }

  .seccion-bloque {
    margin-bottom: 2.5rem;
  }

  .seccion-bloque h3 {
    margin: 0 0 1rem 0;
    font-size: 1.15rem;
    color: var(--text-primary);
  }

  .diagrama-ascii {
    background: #06090d;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1rem;
    overflow-x: auto;
  }

  pre {
    margin: 0;
    font-family: var(--font-mono);
    color: #38bdf8;
    font-size: 0.82rem;
    line-height: 1.4;
  }

  .tabla-specs {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
  }

  .tabla-specs th, .tabla-specs td {
    padding: 0.85rem 1rem;
    border: 1px solid var(--border-color);
    text-align: left;
  }

  .tabla-specs th {
    background: var(--bg-surface);
    color: var(--text-secondary);
  }

  .tabla-specs td {
    color: var(--text-secondary);
    line-height: 1.5;
  }

  .tabla-specs td strong {
    color: var(--text-primary);
  }

  .tabla-specs code {
    background: #06090d;
    color: #a855f7;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-family: var(--font-mono);
  }

  .codigo-box {
    background: #06090d;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1.25rem;
  }

  .codigo-box code {
    color: #4ade80;
    font-family: var(--font-mono);
    font-size: 0.9rem;
  }
</style>
