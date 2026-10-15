# Sección 03 — Carga de Datos en Servidor (`load`), Tipado y Manejo de Errores

> **Basado en la documentación oficial:** [svelte.dev/docs/kit/load](https://svelte.dev/docs/kit/load)

---

## 3.1 La Filosofía de Carga de Datos en SvelteKit

En aplicaciones frontend tradicionales (como React o Svelte puro con Vite), el patrón habitual para cargar datos era:
1. Montar el componente con un estado vacío (`let datos = []`, `let cargando = true`).
2. En un hook del cliente (`onMount` o `useEffect`), disparar una petición `fetch('/api/...')`.
3. Esperar la respuesta y actualizar el estado, provocando parpadeos (*spinners*) y empeorando el SEO.

**SvelteKit elimina este problema de raíz mediante las funciones `load`:**
Los datos se resuelven **antes** de que el componente comience a renderizarse. El HTML resultante ya contiene los datos embebidos desde el servidor.

---

## 3.2 `+page.server.js` vs `+page.js`: ¿Cuál debo usar?

Existen dos tipos de funciones `load`:

| Característica | `+page.server.js` (Server Load) | `+page.js` (Universal Load) |
|---|---|---|
| **Dónde se ejecuta** | **100% en el Servidor** | En servidor durante SSR inicial; en cliente en navegaciones SPA |
| **Acceso a base de datos** | Sí (SQLite, PostgreSQL, ORMs, drivers binarios) | No (expondría contraseñas y drivers al navegador) |
| **Variables secretas** | Acceso a `$env/static/private` (API keys privadas) | Solo `$env/static/public` |
| **Cookies y Sesiones** | Lectura y escritura de cookies HTTP-only | Solo lectura de cookies no protegidas |
| **Uso recomendado** | Conexión con hardware/APIs protegidas, DBs, Auth | Fetch a APIs públicas, transformaciones ligeras en cliente |

> **Regla práctica para ingeniería:** Si interactúas con una base de datos o un servicio que requiere credenciales privadas, usa siempre **`+page.server.js`**.

---

## 3.3 El Objeto `event` en la función `load`

La función `load` recibe un parámetro de evento con múltiples utilidades integradas:

```javascript
// src/routes/sensores/[id]/+page.server.js
export async function load({ params, url, fetch, cookies, locals }) {
  const { id } = params;                     // Parámetro de ruta [id]
  const detalle = url.searchParams.get('v'); // Query params (?v=completo)
  
  // Consulta directa a la base de datos o API interna
  const sensor = await db.sensores.buscarPorTag(id);

  return {
    sensor,
    modoDetallado: detalle === 'completo'
  };
}
```

---

## 3.4 Consumo de Datos en Svelte 5 con `$props()`

Los datos retornados por la función `load` se inyectan en el componente `+page.svelte` como una propiedad llamada `data`:

```svelte
<!-- src/routes/sensores/[id]/+page.svelte -->
<script>
  // En Svelte 5 recibimos 'data' usando la runa $props()
  let { data } = $props();
</script>

<h1>Ficha Técnica: {data.sensor.tag}</h1>
<p>Valor Actual: {data.sensor.valor} {data.sensor.unidad}</p>
<p>Última calibración: {data.sensor.fechaCalibracion}</p>
```

---

## 3.5 Control de Flujo: Errores (`error`) y Redirecciones (`redirect`)

SvelteKit incluye helpers especializados para abortar la navegación cuando algo sale mal:

### 3.5.1 Disparar un Error HTTP (`error`)
Si un sensor solicitado no existe en la base de datos, lanzamos un error 404 estructurado:

```javascript
import { error } from '@sveltejs/kit';

export async function load({ params }) {
  const sensor = await db.obtener(params.id);

  if (!sensor) {
    // Retorna código HTTP 404 con mensaje descriptivo
    error(404, {
      message: `El sensor con tag '${params.id}' no fue hallado en el bus de campo.`,
      codigoError: 'ERR_SENSOR_NOT_FOUND'
    });
  }

  return { sensor };
}
```

### 3.5.2 Redirigir al Usuario (`redirect`)
Si el usuario no tiene permisos o un parámetro ha cambiado de nombre:

```javascript
import { redirect } from '@sveltejs/kit';

export async function load({ locals }) {
  if (!locals.operadorAutenticado) {
    // Redirige al login con código 303 (See Other)
    redirect(303, '/login');
  }
}
```

---

## 3.6 Captura de Errores Visuales: `+error.svelte`

Cuando se dispara un `error(404, ...)`, SvelteKit busca el archivo `+error.svelte` más cercano en la jerarquía para mostrar una vista amigable en lugar de una pantalla blanca:

```svelte
<!-- src/routes/+error.svelte -->
<script>
  import { page } from '$app/state';
</script>

<div class="pantalla-error">
  <h1>Error {page.status}</h1>
  <p>{page.error?.message ?? 'Ocurrió una anomalía no identificada.'}</p>
  <a href="/">Volver a la consola principal</a>
</div>
```

---

## Archivos de Ejemplo en esta Sección

- [`src/routes/+page.server.js`](./src/routes/+page.server.js) — Carga asíncrona en servidor de lista de sensores con cálculo de métricas agregadas.
- [`src/routes/+page.svelte`](./src/routes/+page.svelte) — Vista reactiva en Svelte 5 consumiendo `let { data } = $props()`.
- [`src/routes/sensores/[id]/+page.server.js`](./src/routes/sensores/[id]/+page.server.js) — Carga individual con validación de existencia y lanzamiento de `error(404)`.
- [`src/routes/sensores/[id]/+page.svelte`](./src/routes/sensores/[id]/+page.svelte) — Ficha técnica detallada del sensor.
- [`src/routes/+error.svelte`](./src/routes/+error.svelte) — Página de captura visual de errores HTTP 404/500.

---

## Ejercicios Prácticos

1. **Fácil:** En `src/routes/+page.server.js`, agrega a cada sensor una propiedad `bateriaRestante` (número entre 0 y 100) y muéstrala en la tarjeta de `+page.svelte` con una barra visual de color verde/amarillo/rojo.
2. **Medio:** Implementa filtrado por URL: en `src/routes/+page.server.js`, lee el parámetro `url.searchParams.get('tipo')` (ej. `?tipo=temperatura`) y filtra la lista de sensores antes de enviarla al cliente.
3. **Difícil:** Simula un fallo de red o tiempo de espera en el servidor: si el ID solicitado es `sensor-caido`, lanza un `error(503, { message: 'El nodo no responde a los pings en el bus RS-485' })` y personaliza `+error.svelte` para mostrar un botón de reintento.

---

*<- [Sección 02: Layouts](../02-layouts-y-anidacion/) · [README Principal](../README.md) · [Sección 04: Form Actions ->](../04-form-actions-y-mutaciones/)*
