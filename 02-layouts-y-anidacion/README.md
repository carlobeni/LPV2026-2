# Sección 02 — Layouts, Anidación y UI Shells en SvelteKit

> **Basado en la documentación oficial:** [svelte.dev/docs/kit/routing#layout](https://svelte.dev/docs/kit/routing#layout)

---

## 2.1 ¿Qué es un Layout y por qué es fundamental?

En una aplicación web convencional, cambiar de página suele implicar recargar toda la interfaz: la barra de navegación superior, los menús laterales, el pie de página y los estilos globales. Esto produce parpadeos molestos (*layout shift*) y destruye el estado local (como el texto escrito en un buscador o el estado colapsado de un menú).

Un **Layout** (`+layout.svelte`) en SvelteKit es un componente envoltorio que:
1. Permanece montado en el DOM entre navegaciones.
2. No se vuelve a renderizar cuando el usuario cambia entre rutas hermanas.
3. Proporciona una interfaz compartida (*UI Shell*) persistente.

---

## 2.2 El Gran Cambio en Svelte 5: De `<slot />` a Snippets `{@render children()}`

En versiones anteriores de Svelte (Svelte 3 y 4), los layouts utilizaban la etiqueta `<slot />` para indicar dónde debía renderizarse la página hija.

En **Svelte 5 con Runes**, los slots han sido reemplazados por el sistema de **Snippets**, que es más tipado, flexible y eficiente:

```svelte
<!-- src/routes/+layout.svelte (Svelte 5) -->
<script>
  // Recibimos 'children' como prop a través de la runa $props()
  let { children } = $props();
</script>

<nav>
  <a href="/">Inicio</a>
  <a href="/sensores">Sensores</a>
</nav>

<main>
  <!-- Renderizamos el snippet del contenido hijo -->
  {@render children()}
</main>

<footer>
  <p>LPV 2026-2 · FIUNA</p>
</footer>
```

> **Aviso de Migración:** Si intentas usar `<slot />` en un proyecto Svelte 5 configurado con runes, el compilador emitirá una advertencia de obsolescencia. Siempre usa `let { children } = $props()` y `{@render children()}`.

---

## 2.3 Jerarquía de Layouts Anidados

Los layouts se heredan en cascada hacia abajo por el árbol de carpetas:

```
src/routes/
├── +layout.svelte              <- [Layout Raíz]: Navbar global y estilos base
├── +page.svelte                <- Envuelto por [Layout Raíz]
└── (admin)/
    ├── +layout.svelte          <- [Sub-layout Admin]: Sidebar y panel de permisos
    ├── monitoreo/
    │   └── +page.svelte        <- Envuelto por [Layout Raíz] + [Sub-layout Admin]
    └── calibracion/
        └── +page.svelte        <- Envuelto por [Layout Raíz] + [Sub-layout Admin]
```

Cuando un usuario navega de `/monitoreo` a `/calibracion`:
- El **Layout Raíz** no se recarga.
- El **Sub-layout Admin** (su barra lateral de herramientas) **tampoco se recarga**.
- Únicamente se desmonta y monta el contenido específico del área de trabajo.

---

## 2.4 Romper la Cadena de Herencia: Reseteo de Layout con `@`

A veces necesitas una página que **no** herede el layout de sus carpetas padre. Por ejemplo, una pantalla de inicio de sesión (`/login`), una vista de impresión o una alerta de parada de emergencia que debe ocupar el 100% de la pantalla sin navbars.

SvelteKit permite romper la herencia mediante el sufijo `@`:

| Archivo | Efecto |
|---|---|
| `+page@.svelte` | Ignora todos los layouts intermedios y hereda **únicamente el Layout Raíz**. |
| `+page@nombre-carpeta.svelte` | Hereda el layout definido en `src/routes/nombre-carpeta/+layout.svelte`. |
| `+layout@.svelte` | Define un sub-layout que no hereda layouts padre, solo el raíz. |

```svelte
<!-- src/routes/(auth)/login/+page@.svelte -->
<!-- Al tener '@', este login NO muestra las barras ni layouts definidos en carpetas intermedias -->
<div class="pantalla-completa">
  <h2>Ingreso de Operador</h2>
  <!-- Formulario de acceso -->
</div>
```

---

## 2.5 Datos Compartidos en Layouts: `+layout.js` / `+layout.server.js`

Al igual que las páginas tienen su `+page.server.js`, los layouts pueden tener un `+layout.server.js`:

```javascript
// src/routes/+layout.server.js
export async function load({ locals }) {
  return {
    usuario: locals.user ?? null,
    estadoSistema: "NORMAL",
    timestampInicio: Date.now()
  };
}
```

**Ventaja crucial:** Cualquier página o sub-layout hijo puede acceder a los datos del layout padre automáticamente a través de su prop `data`:

```svelte
<!-- src/routes/dashboard/+page.svelte -->
<script>
  let { data } = $props();
</script>

<p>Operador actual: {data.usuario?.nombre ?? 'Anónimo'}</p>
<p>Estado global: {data.estadoSistema}</p>
```

---

## Archivos de Ejemplo en esta Sección

- [`src/routes/+layout.svelte`](./src/routes/+layout.svelte) — Layout raíz con navegación superior persistente y selector de tema.
- [`src/routes/+page.svelte`](./src/routes/+page.svelte) — Vista pública montada en el layout raíz.
- [`src/routes/(admin)/+layout.svelte`](./src/routes/(admin)/+layout.svelte) — Sub-layout con consola lateral de operador y telemetría de bus.
- [`src/routes/(admin)/control/+page.svelte`](./src/routes/(admin)/control/+page.svelte) — Panel de actuadores montado dentro de ambos layouts.
- [`src/routes/(auth)/login/+page@.svelte`](./src/routes/(auth)/login/+page@.svelte) — Login con layout reseteado (`@`) a pantalla completa limpia.

---

## Ejercicios Prácticos

1. **Fácil:** Añade un pie de página en `src/routes/+layout.svelte` que muestre dinámicamente el año actual usando JavaScript y una insignia con el estado de conexión ("🟢 Bus CAN activo").
2. **Medio:** Crea un sub-layout en `src/routes/sensores/+layout.svelte` que contenga una lista lateral fija con 3 sensores (`Sensor PT-100`, `Sensor Caudalímetro`, `Sensor Presión`). Al hacer clic en cualquiera de ellos, debe navegar a su sub-página sin recargar la lista lateral.
3. **Difícil:** Implementa una página de parada de emergencia en `src/routes/emergencia/+page@.svelte` con reseteo total de layout. La pantalla debe tener fondo rojo pulsante, ocupar el 100vw/100vh, y contener un botón para reanudar el sistema que redirija a `/` usando `goto('/')`.

---

*<- [Sección 01: Enrutamiento](../01-enrutamiento-y-paginas/) · [README Principal](../README.md) · [Sección 03: Carga de Datos ->](../03-carga-de-datos-load/)*
