# Sección 06 — Hooks de Servidor (`hooks.server.js`), Middleware y Seguridad

> **Basado en la documentación oficial:** [svelte.dev/docs/kit/hooks](https://svelte.dev/docs/kit/hooks)

---

## 6.1 ¿Qué es un Hook en SvelteKit?

En aplicaciones industriales y sistemas SCADA, existen reglas transversales que deben aplicarse a **todas** las peticiones que llegan al servidor:
- Verificar si la petición contiene una cookie de sesión válida.
- Registrar el tiempo de respuesta de cada consulta (*logging & metrics*).
- Impedir que operadores no autorizados accedan a la calibración de actuadores críticos.
- Inyectar encabezados de seguridad (CORS, CSP, Server-Timing).

En SvelteKit, estas tareas no se repiten en cada archivo `+page.server.js`. Se implementan de forma centralizada a través de los **Hooks** en `src/hooks.server.js`.

---

## 6.2 El Hook `handle`: El Middleware Universal

La función `handle` se ejecuta **en cada petición HTTP** que recibe el servidor SvelteKit, antes de que cualquier función `load` o Form `action` sea invocada:

```
Petición Entrante (HTTP Request)
          │
          ▼
┌─────────────────────────────────┐
│   src/hooks.server.js (handle)  │
│  - Parsea cookies de sesión     │
│  - Define event.locals.user     │
│  - Valida permisos de ruta      │
└─────────────────────────────────┘
          │
          ├──> ¿Ruta protegida sin auth? ──> redirect(303, '/login')
          │
          ▼
┌─────────────────────────────────┐
│   +page.server.js / +server.js  │
│   (Lee event.locals.user)       │
└─────────────────────────────────┘
          │
          ▼
Respuesta Saliente (HTTP Response)
```

### Firma de la función `handle`:
```javascript
// src/hooks.server.js
export async function handle({ event, resolve }) {
  // 1. Código ANTES de resolver la ruta (inspección de cookies, headers)
  const token = event.cookies.get('session_id');

  if (token) {
    event.locals.user = await verificarSesion(token);
  } else {
    event.locals.user = null;
  }

  // 2. Ejecución de la ruta mediante resolve()
  const response = await resolve(event);

  // 3. Código DESPUÉS de resolver (inyección de headers)
  response.headers.set('X-Frame-Options', 'DENY');

  return response;
}
```

---

## 6.3 El Objeto `event.locals`

`event.locals` es un objeto especial creado por SvelteKit que existe **únicamente durante el ciclo de vida de la petición actual**. Es el lugar oficial para almacenar información del usuario autenticado, roles o configuración de sesión.

Cualquier archivo de servidor (`+page.server.js`, `+layout.server.js`, `+server.js`) puede leer `locals`:

```javascript
// src/routes/+layout.server.js
export async function load({ locals }) {
  // Compartimos el usuario autenticado con todos los layouts y páginas hijas
  return {
    usuario: locals.user
  };
}
```

---

## 6.4 Declaración de Tipos en `src/app.d.ts`

Para que el editor (y TypeScript / JSDoc) reconozca la estructura de `event.locals`:

```typescript
// src/app.d.ts
declare global {
  namespace App {
    interface Locals {
      user: {
        id: string;
        nombre: string;
        rol: 'operador' | 'ingeniero' | 'administrador';
      } | null;
    }
  }
}

export {};
```

---

## 6.5 Medición de Rendimiento con `Server-Timing`

Podemos medir con precisión milimétrica cuánto demora el servidor en procesar cada petición y enviar esa métrica al navegador en la pestaña *Network* de DevTools:

```javascript
// src/hooks.server.js
export async function handle({ event, resolve }) {
  const inicio = performance.now();

  const response = await resolve(event);

  const duracionMs = (performance.now() - inicio).toFixed(2);
  response.headers.set('Server-Timing', `total;dur=${duracionMs};desc="Procesamiento SvelteKit"`);

  return response;
}
```

---

## 6.6 Captura Global de Fallos: `handleError`

Si ocurre una excepción no capturada en cualquier parte del servidor (por ejemplo, una base de datos inaccesible o un error de sintaxis), SvelteKit invoca `handleError`:

```javascript
// src/hooks.server.js
export function handleError({ error, event, status, message }) {
  console.error(`[ALERTA CRÍTICA SCADA] Error ${status} en ${event.url.pathname}:`, error);

  return {
    message: 'Ocurrió una anomalía crítica en el servidor de control.',
    errorId: crypto.randomUUID()
  };
}
```

---

## Archivos de Ejemplo en esta Sección

- [`src/hooks.server.js`](./src/hooks.server.js) — Middleware con autenticación basada en cookies, protección de rutas y medición `Server-Timing`.
- [`src/app.d.ts`](./src/app.d.ts) — Definición de interfaz para `App.Locals`.
- [`src/routes/+layout.server.js`](./src/routes/+layout.server.js) — Propagación de sesión a la interfaz de usuario.
- [`src/routes/+page.svelte`](./src/routes/+page.svelte) — Panel de simulación de inicio y cierre de sesión con selector de roles.
- [`src/routes/admin/calibracion-segura/+page.svelte`](./src/routes/admin/calibracion-segura/+page.svelte) — Zona restringida que requiere rol `administrador`.

---

## Ejercicios Prácticos

1. **Fácil:** En `src/hooks.server.js`, añade un encabezado de seguridad personalizado a todas las respuestas: `X-Mecatronica-Segura: FIUNA-2026`.
2. **Medio:** Crea una regla en `src/hooks.server.js` que registre en la consola de Node.js la fecha, método HTTP, URL y tiempo de respuesta de cada petición entrante: `[2026-10-15 18:30] GET /api/sensores -> 200 (4.2ms)`.
3. **Difícil:** Implementa bloqueo por mantenimiento global: si existe una cookie `mantenimiento=true` y la ruta solicitada no es `/mantenimiento`, redirige automáticamente al usuario a `/mantenimiento`.

---

*<- [Sección 05: APIs y Streaming](../05-api-endpoints-server-routes/) · [README Principal](../README.md) · [Sección 07: Proyecto Avanzado ->](../07-proyecto-avanzado-dashboard/)*
