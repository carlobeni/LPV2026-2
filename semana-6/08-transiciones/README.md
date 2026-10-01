# Sección 08 — Transiciones y Animaciones

> 📖 Referencia:
> - [svelte.dev/tutorial/svelte/transition](https://svelte.dev/tutorial/svelte/transition)
> - [svelte.dev/tutorial/svelte/adding-parameters-to-transitions](https://svelte.dev/tutorial/svelte/adding-parameters-to-transitions)
> - [svelte.dev/tutorial/svelte/in-and-out](https://svelte.dev/tutorial/svelte/in-and-out)
> - [svelte.dev/tutorial/svelte/animations](https://svelte.dev/tutorial/svelte/animations)

---

## 8.1 La Directiva `transition:`

Svelte incluye transiciones CSS animadas integradas. Se activan **automáticamente** cuando un elemento entra o sale del DOM (vía `{#if}`):

```svelte
<script>
  import { fade } from 'svelte/transition';
  let visible = $state(true);
</script>

<button onclick={() => visible = !visible}>Toggle</button>

{#if visible}
  <!-- transition:fade se aplica tanto al entrar como al salir -->
  <p transition:fade>Aparezco y desaparezco con fade</p>
{/if}
```

---

## 8.2 Transiciones Incluidas en Svelte

Svelte incluye varias transiciones listas para usar:

```svelte
<script>
  import { fade, fly, slide, scale, blur, draw } from 'svelte/transition';
</script>

<!-- Fade: opacidad 0 → 1 -->
<div transition:fade>...</div>

<!-- Fly: mueve + fade -->
<div transition:fly={{ x: -200, y: 0, duration: 400 }}>...</div>

<!-- Slide: despliega/colapsa verticalmente -->
<div transition:slide={{ duration: 300 }}>...</div>

<!-- Scale: zoom in/out -->
<div transition:scale={{ start: 0.5 }}>...</div>

<!-- Blur: desenfoque -->
<div transition:blur={{ amount: 10 }}>...</div>
```

---

## 8.3 Entradas y Salidas Separadas con `in:` y `out:`

Puedes definir diferentes animaciones para la entrada y la salida:

```svelte
<script>
  import { fly, fade } from 'svelte/transition';
</script>

{#if visible}
  <!-- Entra volando desde abajo, sale con fade -->
  <div in:fly={{ y: 50, duration: 300 }} out:fade={{ duration: 200 }}>
    Contenido con transiciones asimétricas
  </div>
{/if}
```

---

## 8.4 Parámetros de Transición

Todas las transiciones aceptan parámetros de configuración:

```svelte
<div transition:fly={{
  x: 0,           // desplazamiento horizontal
  y: -100,        // desplazamiento vertical
  duration: 500,  // duración en ms
  delay: 100,     // retraso en ms
  easing: cubicOut // función de easing (de svelte/easing)
}}>
  Contenido
</div>
```

---

## 8.5 Directiva `animate:flip` para Listas

Para animar el reordenamiento de elementos en `{#each}`:

```svelte
<script>
  import { flip } from 'svelte/animate';
  import { fade } from 'svelte/transition';

  let items = $state(["A", "B", "C"]);

  function mezclar() {
    items = items.sort(() => Math.random() - 0.5);
  }
</script>

<button onclick={mezclar}>Mezclar</button>

<ul>
  {#each items as item (item)}
    <!-- animate:flip: anima el movimiento cuando el orden cambia -->
    <li animate:flip={{ duration: 300 }} transition:fade>
      {item}
    </li>
  {/each}
</ul>
```

> 💡 `animate:flip` requiere que los elementos tengan una **key** en el `{#each}`.

---

## 8.6 Funciones de Easing

```svelte
<script>
  import { cubicIn, cubicOut, elasticOut, bounceOut } from 'svelte/easing';
</script>

<div transition:fly={{ y: 100, easing: elasticOut }}>
  Efecto elástico al entrar
</div>
```

| Función | Descripción |
|---------|-------------|
| `linear` | Velocidad constante |
| `cubicIn` | Empieza lento, termina rápido |
| `cubicOut` | Empieza rápido, termina lento |
| `cubicInOut` | Lento-rápido-lento |
| `elasticOut` | Rebote elástico al terminar |
| `bounceOut` | Rebote al terminar |

---

## 🧪 Mini Página: Lista con Transiciones

Una lista de tareas donde los elementos entran y salen con transiciones, y se pueden reordenar con animaciones.

**Archivo:** [`App.svelte`](./App.svelte)

---

## ✏️ Ejercicios

1. **Fácil:** Cambia la transición de entrada de `fly` a `scale` y observa la diferencia.
2. **Medio:** Agrega un selector de transición para que el usuario pueda elegir entre `fade`, `fly`, `slide` y `scale`.
3. **Difícil:** Implementa una animación personalizada usando la API de transición de bajo nivel de Svelte.

---

*← [Sección 07: Estilos](../07-estilos/) · [README principal →](../README.md)*
