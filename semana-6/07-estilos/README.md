# Sección 07 — Clases y Estilos Dinámicos

> 📖 Referencia:
> - [svelte.dev/tutorial/svelte/classes](https://svelte.dev/tutorial/svelte/classes)
> - [svelte.dev/tutorial/svelte/styles](https://svelte.dev/tutorial/svelte/styles)
> - [svelte.dev/tutorial/svelte/component-styles](https://svelte.dev/tutorial/svelte/component-styles)

---

## 7.1 Clases CSS Dinámicas

### Forma 1: Expresión ternaria
```svelte
<script>
  let activo = $state(false);
</script>

<button class={activo ? "btn activo" : "btn"}>Click</button>
```

### Forma 2: Directiva `class:nombre` (recomendada)
```svelte
<button
  class="btn"
  class:activo={activo}
  class:grande={tamano === "lg"}
>
  Click
</button>
```

> 💡 La directiva `class:nombre={condicion}` agrega la clase `nombre` solo cuando la condición es `true`. Es más legible que las expresiones ternarias.

### Shorthand cuando variable y clase tienen el mismo nombre:
```svelte
<script>
  let activo = $state(true); // Mismo nombre que la clase
</script>

<!-- Equivale a class:activo={activo} -->
<div class:activo>Contenido</div>
```

---

## 7.2 Directiva `style:propiedad`

Puedes aplicar propiedades CSS individuales de forma dinámica:

```svelte
<script>
  let color = $state("#4f46e5");
  let tamaño = $state(16);
  let visible = $state(true);
</script>

<p
  style:color={color}
  style:font-size="{tamaño}px"
  style:opacity={visible ? 1 : 0}
>
  Texto estilizado dinámicamente
</p>
```

### VS el atributo `style` directo:
```svelte
<!-- Menos recomendado (concatenación de strings) -->
<p style="color: {color}; font-size: {tamaño}px">...</p>

<!-- Más recomendado (directivas individuales) -->
<p style:color={color} style:font-size="{tamaño}px">...</p>
```

---

## 7.3 Variables CSS Custom (CSS Custom Properties)

Una técnica poderosa es pasar valores de Svelte a CSS como variables:

```svelte
<script>
  let hue = $state(220); // Tono del color HSL
</script>

<div style="--color-principal: hsl({hue}, 70%, 60%)">
  <p class="texto-principal">Este texto usa la variable CSS</p>
</div>

<style>
  .texto-principal {
    color: var(--color-principal);
    border-left: 4px solid var(--color-principal);
    padding-left: 1rem;
  }
</style>
```

---

## 7.4 Estilos Globales vs Scoped

```svelte
<style>
  /* Scoped: solo afecta a este componente */
  p { color: red; }

  /* Global: afecta a toda la app */
  :global(body) { margin: 0; }
  :global(.clase-global) { font-weight: bold; }
</style>
```

---

## 7.5 Paso de Estilos a Componentes Hijos

Para pasar variables CSS a componentes hijos, usa el atributo especial `--`:

```svelte
<!-- Padre -->
<BotonColoreado --color-boton="#10b981" />
```

```svelte
<!-- BotonColoreado.svelte -->
<button class="boton">Presionar</button>

<style>
  .boton {
    /* Usa la variable CSS pasada por el padre */
    background: var(--color-boton, #4f46e5);
    color: white;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.5rem;
  }
</style>
```

---

## 🧪 Mini Página: Selector de Tema

Una interfaz con toggle entre tema claro y oscuro, más un selector de color de acento.

**Archivo:** [`App.svelte`](./App.svelte)

---

## ✏️ Ejercicios

1. **Fácil:** Agrega un tercer tema "sepia" con colores cálidos.
2. **Medio:** Guarda el tema seleccionado en `localStorage` para que persista al recargar.
3. **Difícil:** Implementa un selector de colores completo con sliders HSL.

---

*← [Sección 06: Bindings](../06-bindings/) · [Sección 08: Transiciones →](../08-transiciones/)*
