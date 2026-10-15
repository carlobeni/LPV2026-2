# Sección 05 — Endpoints de API REST, Rutas de Servidor (`+server.js`) y Streaming

> **Basado en la documentación oficial:** [svelte.dev/docs/kit/routing#server](https://svelte.dev/docs/kit/routing#server)

---

## 5.1 ¿Qué es una Ruta de Servidor (`+server.js`)?

Mientras que `+page.svelte` y `+page.server.js` están diseñados para devolver HTML y renderizar vistas de usuario, un archivo **`+server.js`** convierte una ruta en un **Endpoint de API puro**.

En lugar de renderizar componentes, `+server.js` exporta funciones con los nombres exactos de los métodos HTTP correspondientes:
- `export async function GET({ url, params }) { ... }`
- `export async function POST({ request }) { ... }`
- `export async function PUT({ request, params }) { ... }`
- `export async function PATCH({ request, params }) { ... }`
- `export async function DELETE({ params }) { ... }`

---

## 5.2 ¿Cuándo usar Form Actions (`+page.server.js`) vs Endpoints API (`+server.js`)?

| Criterio | Form Actions (`+page.server.js`) | API Endpoints (`+server.js`) |
|---|---|---|
| **Destinatario principal** | Páginas y componentes de tu propia aplicación | Clientes externos, apps móviles, scripts Python o microservicios |
| **Integración con formularios** | Nativa (`<form method="POST">`) con `use:enhance` | Requiere invocar `fetch()` manualmente en JavaScript |
| **Revalidación de datos** | **Automática:** actualiza los `load` de la pantalla | **Manual:** el cliente debe invalidar o recargar el estado |
| **Streaming / SSE** | No aplicable | Sí (compatible con `ReadableStream` y `EventSource`) |
| **Descarga de archivos binarios** | No recomendado | Ideal (PDFs, CSVs, imágenes dinámicas) |

---

## 5.3 El Helper `json()` y los Estándares de la Web API

SvelteKit utiliza las clases estándar de los navegadores modernos (`Request`, `Response`, `Headers`, `URL`). Para devolver respuestas JSON tipadas de forma concisa, se provee el helper `json()`:

```javascript
// src/routes/api/sensores/+server.js
import { json } from '@sveltejs/kit';

export async function GET({ url }) {
  const limite = Number(url.searchParams.get('limite') ?? '10');
  const datos = await obtenerLecturasDeHardware(limite);

  return json(datos, {
    status: 200,
    headers: {
      'Cache-Control': 'max-age=5, public'
    }
  });
}

export async function POST({ request }) {
  const payload = await request.json(); // Parsea el cuerpo JSON entrante

  if (!payload.tag) {
    return json({ error: 'Falta el campo tag' }, { status: 400 });
  }

  const nuevo = await guardarEnBaseDeDatos(payload);
  return json(nuevo, { status: 201 });
}
```

---

## 5.4 Descarga Directa de Archivos (CSV, Binarios)

Para generar reportes descargables al vuelo (por ejemplo, exportación de auditoría para ingenieros de planta):

```javascript
// src/routes/api/exportar/csv/+server.js
export async function GET() {
  const filasCSV = [
    "Timestamp,Tag,Magnitud,Unidad",
    "2026-10-15T18:00:00Z,PT100-HORNO-1,245.8,°C",
    "2026-10-15T18:00:01Z,PIEZO-TUBERIA-B,6.2,bar"
  ].join("\n");

  return new Response(filasCSV, {
    status: 200,
    headers: {
      'Content-Type': 'text/csv; charset=utf-8',
      'Content-Disposition': 'attachment; filename="telemetria_planta_2026.csv"'
    }
  });
}
```

---

## 5.5 Streaming en Tiempo Real con Server-Sent Events (SSE)

Para transmitir mediciones continuas de sensores a un dashboard sin abrir conexiones pesadas de WebSocket:

```javascript
// src/routes/api/telemetria/stream/+server.js
export function GET() {
  let intervalo;

  const stream = new ReadableStream({
    start(controller) {
      intervalo = setInterval(() => {
        const muestra = {
          temperatura: (80 + Math.random() * 5).toFixed(2),
          presion: (4.5 + Math.random() * 0.4).toFixed(2),
          timestamp: Date.now()
        };

        const mensaje = `data: ${JSON.stringify(muestra)}\n\n`;
        controller.enqueue(new TextEncoder().encode(mensaje));
      }, 1000);
    },
    cancel() {
      clearInterval(intervalo);
    }
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    }
  });
}
```

En el cliente Svelte 5, el consumo se realiza de forma limpia mediante `EventSource`:

```svelte
<script>
  let lecturas = $state([]);

  $effect(() => {
    const es = new EventSource('/api/telemetria/stream');

    es.onmessage = (e) => {
      const data = JSON.parse(e.data);
      lecturas = [...lecturas.slice(-19), data];
    };

    return () => es.close(); // Limpieza al desmontar
  });
</script>
```

---

## Archivos de Ejemplo en esta Sección

- [`src/routes/api/sensores/+server.js`](./src/routes/api/sensores/+server.js) — Endpoints GET y POST con query params y validación.
- [`src/routes/api/sensores/[id]/+server.js`](./src/routes/api/sensores/[id]/+server.js) — Endpoint dinámico GET y DELETE (204 No Content).
- [`src/routes/api/telemetria/stream/+server.js`](./src/routes/api/telemetria/stream/+server.js) — Endpoint SSE con `ReadableStream`.
- [`src/routes/api/exportar/csv/+server.js`](./src/routes/api/exportar/csv/+server.js) — Generación al vuelo de archivo CSV.
- [`src/routes/+page.svelte`](./src/routes/+page.svelte) — Dashboard cliente consumiendo las APIs REST y la transmisión SSE.

---

## Ejercicios Prácticos

1. **Fácil:** Agrega soporte para el método `PUT` en `src/routes/api/sensores/[id]/+server.js` que permita actualizar el valor y unidad del sensor especificado.
2. **Medio:** En `src/routes/api/exportar/csv/+server.js`, permite filtrar las columnas agregando un query param `?columnas=tag,valor` para que el archivo CSV solo incluya las variables seleccionadas por el operario.
3. **Difícil:** Implementa un limitador de tasa de peticiones (*Rate Limiter*) en memoria dentro de `src/routes/api/sensores/+server.js`: si una misma IP o cliente realiza más de 5 peticiones POST en menos de 10 segundos, devuelve un código HTTP 429 Too Many Requests con un header `Retry-After: 10`.

---

*<- [Sección 04: Form Actions](../04-form-actions-y-mutaciones/) · [README Principal](../README.md) · [Sección 06: Hooks ->](../06-hooks-y-middleware/)*
