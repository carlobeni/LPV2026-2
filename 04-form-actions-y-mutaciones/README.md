# Sección 04 — Form Actions, Progressive Enhancement (`use:enhance`) y Mutaciones

> **Basado en la documentación oficial:** [svelte.dev/docs/kit/form-actions](https://svelte.dev/docs/kit/form-actions)

---

## 4.1 La Filosofía de SvelteKit: ¿Por qué Form Actions en lugar de APIs REST manuales?

En el desarrollo web tradicional con React, Vue o Angular, modificar datos (*mutaciones*) suele requerir:
1. Crear un endpoint manual en `/api/crear-sensor` (POST).
2. En el cliente, interceptar el submit con `e.preventDefault()`.
3. Extraer manualmente cada campo (`const tag = input.value`).
4. Ejecutar un `fetch('/api/crear-sensor', { method: 'POST', body: JSON.stringify(...) })`.
5. Manejar manualmente el token CSRF, las respuestas de error y el estado de carga.
6. Volver a llamar a la función que cargaba la lista para que la pantalla se actualice (*revalidación manual*).

**SvelteKit simplifica todo este flujo radicalmente con las Form Actions:**
- Las mutaciones se declaran en el mismo archivo `+page.server.js`.
- Funcionan con elementos HTML estándar `<form method="POST">`.
- **Revalidación automática:** SvelteKit vuelve a ejecutar automáticamente todas las funciones `load` activas tras una mutación exitosa, manteniendo la interfaz 100% sincronizada sin escribir código extra.
- **Resiliencia progresiva:** Funcionan incluso si el navegador tiene JavaScript bloqueado o una conexión inestable.

---

## 4.2 Anatomía de una Form Action en `+page.server.js`

Las acciones se exportan mediante un objeto `actions`:

```javascript
// src/routes/+page.server.js
import { fail } from '@sveltejs/kit';

export const actions = {
  // Acción por defecto (se ejecuta si el form no especifica ?/accion)
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const tag = data.get('tag');

    if (!tag || tag.toString().trim() === '') {
      return fail(400, {
        error: 'El tag del instrumento es obligatorio.',
        valoresPrevios: { tag }
      });
    }

    await db.sensores.guardar({ tag });

    return { exito: true };
  }
};
```

---

## 4.3 Acciones Nominadas (Named Actions)

Si una misma página permite realizar varias operaciones distintas (por ejemplo, **Crear**, **Calibrar** y **Eliminar**), usamos acciones nombradas:

```javascript
// src/routes/+page.server.js
export const actions = {
  crear: async ({ request }) => { /* ... */ },
  calibrar: async ({ request }) => { /* ... */ },
  eliminar: async ({ request }) => { /* ... */ }
};
```

En el componente Svelte, vinculamos cada formulario a su acción correspondiente mediante el atributo `action="?/nombre"`:

```svelte
<!-- Formulario para calibrar -->
<form method="POST" action="?/calibrar">
  <input type="hidden" name="id" value="temp-01" />
  <button type="submit">Calibrar Sensor</button>
</form>

<!-- Formulario para eliminar -->
<form method="POST" action="?/eliminar">
  <input type="hidden" name="id" value="temp-01" />
  <button type="submit">Eliminar</button>
</form>
```

---

## 4.4 Validación y Manejo de Errores con `fail()`

Cuando la validación en el servidor falla, **nunca** debes lanzar un error HTTP 500. En su lugar, usa el helper `fail(status, data)` de `@sveltejs/kit`:
- Envía el código de estado apropiado (como 400 Bad Request o 422 Unprocessable Entity).
- Retorna los datos de error al componente sin abortar la página.
- Permite devolver los `valoresPrevios` para no borrar lo que el usuario ya había escrito.

---

## 4.5 Consumo del Feedback en Svelte 5 con `$props()`

El resultado de una Form Action se recibe en el componente mediante la prop `form`:

```svelte
<!-- src/routes/+page.svelte -->
<script>
  let { data, form } = $props();
</script>

{#if form?.error}
  <div class="mensaje-error">
    {form.error}
  </div>
{/if}

{#if form?.exito}
  <div class="mensaje-exito">
    Instrumento registrado satisfactoriamente.
  </div>
{/if}

<input name="tag" value={form?.valoresPrevios?.tag ?? ''} />
```

---

## 4.6 Mejora Progresiva con `use:enhance`

Para convertir un formulario nativo en una experiencia interactiva sin recarga de página (Single Page App):

```svelte
<script>
  import { enhance } from '$app/forms';

  let guardando = $state(false);
</script>

<!-- use:enhance intercepta el submit vía fetch manteniendo la accesibilidad nativa -->
<form 
  method="POST" 
  action="?/crear" 
  use:enhance={() => {
    // Código ejecutado inmediatamente antes de enviar
    guardando = true;

    return async ({ update }) => {
      // Código ejecutado al recibir la respuesta del servidor
      guardando = false;
      await update(); // Aplica la revalidación automática de SvelteKit
    };
  }}
>
  <button disabled={guardando}>
    {guardando ? 'Guardando en Servidor...' : 'Registrar Sensor'}
  </button>
</form>
```

---

## Archivos de Ejemplo en esta Sección

- [`src/routes/+page.server.js`](./src/routes/+page.server.js) — Acciones `crear`, `calibrar` y `eliminar` con validaciones de tipos físicos y límites de escala.
- [`src/routes/+page.svelte`](./src/routes/+page.svelte) — Formulario interactivo con `use:enhance`, spinners reactivos, validación en tiempo real y eliminación optimista.

---

## Ejercicios Prácticos

1. **Fácil:** Agrega un campo numérico `umbralAlerta` en el formulario de creación. En el servidor, valida que sea mayor a 0; si es menor o igual, retorna `fail(400, { error: 'El umbral debe ser un valor físico positivo' })`.
2. **Medio:** Implementa una acción nominada `?/reiniciar` que reciba un `id` y simule un reinicio del nodo con una demora de 1 segundo (`await new Promise(r => setTimeout(r, 1000))`). En la interfaz, muestra un spinner animado en el botón específico mientras se procesa.
3. **Difícil:** Agrega interfaz de usuario optimista (*Optimistic UI*): al pulsar eliminar, quita el elemento de la lista local inmediatamente en el cliente; si la acción en el servidor falla, revierte la lista a su estado anterior y muestra un toast de error.

---

*<- [Sección 03: Carga de Datos](../03-carga-de-datos-load/) · [README Principal](../README.md) · [Sección 05: API Endpoints ->](../05-api-endpoints-server-routes/)*
