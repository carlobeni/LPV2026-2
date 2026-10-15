# Sección 01 — Enrutamiento Basado en Archivos y Páginas en SvelteKit

> **Basado en la documentación oficial:** [svelte.dev/docs/kit/routing](https://svelte.dev/docs/kit/routing)

---

## 1.1 De Svelte a SvelteKit: ¿Por qué necesitamos un Framework Full-stack?

En la **Semana 6**, aprendimos los fundamentos reactivos de **Svelte 5** (Runes, componentes, props, eventos y transiciones). Sin embargo, una aplicación real de ingeniería requiere más que componentes aislados:

1. **Enrutamiento (Routing):** Permitir URLs navegables (`/dashboard`, `/sensores/42`, `/configuracion`) con historial del navegador (atrás/adelante) y marcadores.
2. **Renderizado en Servidor (SSR - Server-Side Rendering):** El servidor genera el HTML inicial, reduciendo el tiempo de primera carga y permitiendo indexación inmediata.
3. **Carga y Mutación de Datos Unificada:** Conexión segura a bases de datos, APIs externas o hardware embebido sin exponer credenciales en el cliente.
4. **Optimización Automática:** División de código (*code-splitting*), precarga inteligente de páginas al pasar el cursor (*hover prefetching*) y compilación de CSS ultra liviano.

**SvelteKit** es el framework oficial sobre Svelte que resuelve estos desafíos mediante una arquitectura unificada.

---

## 1.2 El Enrutador Basado en el Sistema de Archivos (File-Based Routing)

En SvelteKit, **las carpetas dentro del directorio `src/routes/` definen directamente las URLs de la aplicación**. No existe un archivo central `routes.js` ni listas manuales de expresiones regulares.

### La regla de oro de los archivos con prefijo `+`
Para evitar colisiones entre código de rutas y componentes privados auxiliares, SvelteKit reserva archivos especiales que comienzan con el signo más (`+`):

| Archivo | Rol | Dónde se ejecuta |
|---|---|---|
| `+page.svelte` | Define la vista HTML/interfaz de usuario de la ruta. | Cliente y Servidor (SSR) |
| `+page.js` / `+page.ts` | Función `load` universal para cargar datos. | Servidor (SSR) e hidratado en Cliente |
| `+page.server.js` | Función `load` y Form `actions` exclusivos de servidor. | Únicamente en el Servidor |
| `+layout.svelte` | Envoltorio/Plantilla visual compartida para una ruta y sus subrutas. | Cliente y Servidor (SSR) |
| `+server.js` | Endpoint de API REST independiente (GET, POST, PUT, DELETE). | Únicamente en el Servidor |
| `+error.svelte` | Vista visual de captura de fallos HTTP (404, 500, etc.). | Cliente y Servidor (SSR) |

> **Nota importante:** Cualquier archivo que **NO** empiece con `+` (por ejemplo, `SensorCard.svelte`, `utils.js`) es ignorado por el enrutador y puede usarse de forma segura como componente o helper privado dentro de la carpeta.

---

## 1.3 Tipos de Rutas en SvelteKit

```
src/routes/
├── +page.svelte                     -> /
├── about/
│   └── +page.svelte                 -> /about
├── dispositivos/
│   ├── +page.svelte                 -> /dispositivos
│   └── [id]/
│       └── +page.svelte             -> /dispositivos/1, /dispositivos/motor-01
├── docs/
│   └── [...slug]/
│       └── +page.svelte             -> /docs/sensores/temperatura/pt100
└── reportes/
    └── [[periodo]]/
        └── +page.svelte             -> /reportes, /reportes/2026-q1
```

### 1.3.1 Rutas Estáticas
Una carpeta con un nombre fijo que contiene un `+page.svelte`:
- `src/routes/about/+page.svelte` responde exactamente a la URL `http://localhost:5173/about`.

### 1.3.2 Rutas Dinámicas con Parámetros `[param]`
Cuando una parte de la URL es variable (por ejemplo, el ID de un sensor, el código de un robot o el RUT de un operario), encerramos el nombre del directorio entre corchetes:
- Carpeta: `src/routes/dispositivos/[id]/+page.svelte`
- URLs válidas: `/dispositivos/4001`, `/dispositivos/bomba-hidraulica-2`.

**¿Cómo leer el parámetro en SvelteKit con Svelte 5?**
SvelteKit provee el módulo `$app/state` (o el store tradicional `$app/stores`). En Svelte 5, el acceso es puramente reactivo:

```svelte
<!-- src/routes/dispositivos/[id]/+page.svelte -->
<script>
  import { page } from '$app/state';

  // page.params.id contiene el valor de [id]
  let idDispositivo = $derived(page.params.id);
</script>

<h1>Panel del Dispositivo: {idDispositivo}</h1>
```

### 1.3.3 Rutas Rest / Catch-All `[...param]`
Si necesitas capturar múltiples segmentos de ruta de profundidad arbitraria:
- Carpeta: `src/routes/docs/[...slug]/+page.svelte`
- Coincide con: `/docs/manual`, `/docs/calibracion/sensores/flujo/v1`.
- `page.params.slug` devuelve la cadena completa: `"calibracion/sensores/flujo/v1"`.

### 1.3.4 Parámetros Opcionales `[[param]]`
Si un segmento puede estar o no presente:
- Carpeta: `src/routes/reportes/[[periodo]]/+page.svelte`
- Coincide tanto con `/reportes` (`params.periodo === undefined`) como con `/reportes/octubre-2026` (`params.periodo === "octubre-2026"`).

---

## 1.4 Navegación Eficiente en el Cliente

En SvelteKit **no necesitas una etiqueta `<Link>` propietaria**. Usas la etiqueta estándar de HTML `<a>`:

```svelte
<!-- Enlace HTML estándar: SvelteKit lo intercepta automáticamente como navegación SPA -->
<a href="/dispositivos/42">Ver Sensor 42</a>
```

### 1.4.1 Atributos de Precarga Inteligente (`data-sveltekit-*`)
Puedes optimizar la velocidad percibida por el usuario añadiendo atributos especiales:

```svelte
<!-- Precarga el código JS y los datos en cuanto el puntero se posa sobre el link -->
<a href="/dashboard" data-sveltekit-preload-data="hover">Dashboard</a>

<!-- Precarga inmediatamente cuando el link entra en el viewport visible -->
<a href="/metricas" data-sveltekit-preload-data="tap">Métricas Rápidas</a>

<!-- Fuerza una recarga completa de página del navegador (sin SPA) -->
<a href="/logout" data-sveltekit-reload>Cerrar Sesión</a>
```

### 1.4.2 Navegación Programática con `goto()`
Para redirigir al usuario tras un evento (por ejemplo, después de hacer clic en un botón de parada de emergencia o finalizar un temporizador):

```svelte
<script>
  import { goto } from '$app/navigation';

  function registrarParadaEmergencia() {
    console.warn("Disparo de seguridad ejecutado");
    goto('/alerta-critica');
  }
</script>

<button onclick={registrarParadaEmergencia}>PARADA DE EMERGENCIA</button>
```

---

## 1.5 Grupos de Rutas `(nombre)`

Puedes organizar rutas lógicamente sin alterar la estructura visible de las URLs colocando el nombre del directorio entre paréntesis:

```
src/routes/
├── (publico)/
│   ├── +page.svelte                 -> /
│   └── catalogo/
│       └── +page.svelte             -> /catalogo
└── (operaciones)/
    └── telemetria/
        └── +page.svelte             -> /telemetria
```
Las carpetas `(publico)` y `(operaciones)` no aparecen en la URL final. Son ideales para aplicar diferentes layouts o agrupar módulos del sistema.

---

## Estructura de Ejemplo de esta Sección

En esta carpeta encontrarás los archivos modelo para replicar y probar:
- [`src/routes/+page.svelte`](./src/routes/+page.svelte) — Menú interactivo con selector de parámetros y navegación programática.
- [`src/routes/about/+page.svelte`](./src/routes/about/+page.svelte) — Ruta estática institucional con metadata y navegación relativa.
- [`src/routes/dispositivos/[id]/+page.svelte`](./src/routes/dispositivos/[id]/+page.svelte) — Demostración reactiva de captura de parámetros dinámicos con Svelte 5.
- [`src/routes/docs/[...slug]/+page.svelte`](./src/routes/docs/[...slug]/+page.svelte) — Demostración de ruta comodín (*catch-all*) para manuales técnicos.

---

## Ejercicios Prácticos

1. **Fácil:** Crea una ruta estática en `src/routes/contacto/+page.svelte` con información de soporte técnico del laboratorio de Mecatrónica y añade un enlace con `data-sveltekit-preload-data="hover"` en la página principal.
2. **Medio:** Crea una ruta dinámica `src/routes/motores/[codigo]/+page.svelte`. Si el código contiene la palabra "AC", muestra una insignia azul de "Motor de Corriente Alterna"; si contiene "DC", muestra una insignia roja de "Motor de Corriente Continua".
3. **Difícil:** Implementa una ruta con parámetro opcional `src/routes/historial/[[filtro]]/+page.svelte`. Si el parámetro no está presente, muestra un mensaje indicando "Mostrando todos los registros"; si está presente (por ejemplo, `criticos`), muestra "Filtrado por: criticos" y ofrece botones para navegar entre `hoy`, `semana` y `todos` usando `goto()`.

---

*<- [README Principal](../README.md) · [Sección 02: Layouts y Anidación ->](../02-layouts-y-anidacion/)*
