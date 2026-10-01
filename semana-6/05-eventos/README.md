# Sección 05 — Eventos DOM y Manejadores

> Referencia:
> - [svelte.dev/tutorial/svelte/dom-events](https://svelte.dev/tutorial/svelte/dom-events)
> - [svelte.dev/tutorial/svelte/inline-handlers](https://svelte.dev/tutorial/svelte/inline-handlers)

---

## 5.1 Escuchando Eventos con `on`

En Svelte 5, los eventos se manejan con el atributo `on` + nombre del evento:

```svelte
<!-- onclick, onmouseover, onkeydown, etc. -->
<button onclick={manejarClick}>Haz click</button>
```

> **Svelte 5 vs Svelte 4:** En Svelte 4 se usaba `on:click`. En Svelte 5 se usa `onclick` (sin los dos puntos), igual que el HTML estándar.

---

## 5.2 Funciones Manejadoras

```svelte
<script>
  let mensajes = $state([]);

  function manejarClick() {
    mensajes = [...mensajes, "Botón presionado"];
  }

  // La función recibe automáticamente el objeto Event
  function manejarMouse(evento) {
    console.log(`Posición: X=${evento.clientX}, Y=${evento.clientY}`);
  }
</script>

<button onclick={manejarClick}>Presioname</button>
<div onmousemove={manejarMouse}>Mueve el mouse aquí</div>
```

---

## 5.3 Manejadores Inline (Lambdas)

Para lógica simple, puedes escribir la función directamente en el atributo:

```svelte
<script>
  let contador = $state(0);
</script>

<!-- Función inline (lambda) -->
<button onclick={() => contador++}>+1</button>

<!-- Con parámetros -->
<button onclick={() => agregar("manzana")}>Agregar manzana</button>

<!-- Con el evento -->
<input oninput={(e) => console.log(e.target.value)} />
```

---

## 5.4 Modificadores de Eventos

En Svelte 5, los modificadores se aplican manualmente con la API del DOM:

```svelte
<script>
  function manejarSubmit(e) {
    e.preventDefault();  // <- equivalente al modificador preventDefault
    // procesar el formulario...
  }

  function manejarClick(e) {
    e.stopPropagation();  // <- evita que el evento suba al padre
  }
</script>

<form onsubmit={manejarSubmit}>
  <button type="submit">Enviar</button>
</form>

<div onclick={() => console.log("div")}>
  <button onclick={manejarClick}>No propaga</button>
</div>
```

---

## 5.5 Eventos de Teclado

```svelte
<script>
  let busqueda = $state("");

  function manejarTecla(e) {
    if (e.key === "Enter") {
      console.log("Buscar:", busqueda);
    }
    if (e.key === "Escape") {
      busqueda = "";
    }
  }
</script>

<input
  bind:value={busqueda}
  onkeydown={manejarTecla}
  placeholder="Buscar..."
/>
```

---

## 5.6 Eventos Comunes de HTML

| Evento | Descripción | Ejemplo |
|--------|-------------|---------|
| `onclick` | Click del mouse | Botones, tarjetas |
| `oninput` | Cambio en inputs | Búsqueda en tiempo real |
| `onchange` | Cambio confirmado | Selects, checkboxes |
| `onsubmit` | Envío de formulario | Formularios |
| `onkeydown` | Tecla presionada | Atajos de teclado |
| `onmouseover` | Mouse encima | Tooltips, hover |
| `onfocus` | Elemento enfocado | Validación |
| `onblur` | Elemento desenfocado | Validación |

---

## Mini Página: Formulario de Contacto

Un formulario completo con validación de eventos en tiempo real.

**Archivo:** [`App.svelte`](./App.svelte)

---

## Ejercicios

1. **Fácil:** Agrega un botón "Limpiar formulario" que reinicie todos los campos.
2. **Medio:** Implementa un contador de caracteres para el campo "mensaje" que avise cuando supere los 200 caracteres.
3. **Difícil:** Agrega validación en tiempo real que muestre mensajes de error específicos para cada campo.

---

*<- [Sección 04: Lógica](../04-logica/) · [Sección 06: Bindings ->](../06-bindings/)*
