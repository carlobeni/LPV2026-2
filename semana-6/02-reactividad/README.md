# Sección 02 — Reactividad con `$state` y `$derived`

> Referencia:
> - [svelte.dev/tutorial/svelte/state](https://svelte.dev/tutorial/svelte/state)
> - [svelte.dev/tutorial/svelte/derived-state](https://svelte.dev/tutorial/svelte/derived-state)
> - [svelte.dev/tutorial/svelte/effects](https://svelte.dev/tutorial/svelte/effects)

---

## 2.1 Qué es el Estado

El **estado** es cualquier dato que puede cambiar a lo largo del tiempo y que debe reflejarse en la interfaz.

En Svelte 5, el estado se declara con la **rune** `$state`:

```svelte
<script>
  // Svelte 4 (antiguo)
  let contador = 0;

  // Svelte 5 (nuevo con runes)
  let contador = $state(0);
</script>
```

> **Qué es una "rune":** Son funciones especiales del compilador de Svelte 5 que comienzan con `$`. No son funciones JavaScript normales, sino señales al compilador para activar reactividad.

---

## 2.2 `$state` — Estado Reactivo Básico

Cuando una variable se declara con `$state`, Svelte **rastrea automáticamente** todos los lugares donde se usa y actualiza el DOM cuando cambia:

```svelte
<script>
  let contador = $state(0);

  function incrementar() {
    contador += 1;  // <- Svelte detecta este cambio y actualiza el DOM
  }

  function reiniciar() {
    contador = 0;
  }
</script>

<p>Contador: {contador}</p>
<button onclick={incrementar}>+1</button>
<button onclick={reiniciar}>Reiniciar</button>
```

---

## 2.3 `$derived` — Estado Derivado

Cuando un valor **depende de otro** estado, usamos `$derived`:

```svelte
<script>
  let precio = $state(100);
  let cantidad = $state(3);

  // Se recalcula automáticamente cuando precio o cantidad cambian
  let total = $derived(precio * cantidad);
  let totalConIVA = $derived(total * 1.10);
</script>

<p>Precio unitario: ${precio}</p>
<p>Cantidad: {cantidad}</p>
<p>Total: ${total}</p>
<p>Total con IVA (10%): ${totalConIVA.toFixed(2)}</p>
```

> `$derived` es equivalente a las "propiedades computadas" de Vue o `useMemo` en React, pero mucho más simple.

---

## 2.4 `$effect` — Efectos Secundarios

`$effect` ejecuta código cuando el estado cambia (útil para logs, llamadas a APIs, sincronización con el DOM):

```svelte
<script>
  let nombre = $state("");
  let mensajes = $state([]);

  // Se ejecuta cada vez que `nombre` cambia
  $effect(() => {
    if (nombre.length > 0) {
      console.log(`El nombre cambió a: ${nombre}`);
    }
  });
</script>

<input bind:value={nombre} placeholder="Escribe tu nombre..." />
<p>Hola, {nombre || "desconocido"}!</p>
```

> No uses `$effect` para calcular valores derivados; para eso existe `$derived`.

---

## 2.5 Estado Profundo — Arrays y Objetos

Para arrays y objetos, `$state` también rastrea cambios internos:

```svelte
<script>
  let lista = $state(["manzana", "banana"]);

  function agregar() {
    lista.push("naranja");  // <- Svelte detecta el push()
  }

  function eliminar(indice) {
    lista.splice(indice, 1);  // <- También detecta splice()
  }
</script>

{#each lista as item, i}
  <p>{item} <button onclick={() => eliminar(i)}>x</button></p>
{/each}
<button onclick={agregar}>Agregar naranja</button>
```

---

## 2.6 Comparación: Con y Sin Reactividad

```
Sin $state (no funciona en Svelte 5):       Con $state (funciona correctamente):
-----------------------------------------  --------------------------------------
let contador = 0;                           let contador = $state(0);

function incrementar() {                    function incrementar() {
  contador++;  // El DOM NO se actualiza     contador++;  // El DOM SI se actualiza
}                                           }
```

---

## Mini Página: Contador Interactivo

Un contador con múltiples operaciones para ver la reactividad en acción.

**Archivo:** [`App.svelte`](./App.svelte)

**Para ejecutar:**
```bash
npm create vite@latest semana6-02 -- --template svelte
cd semana6-02
# Reemplaza src/App.svelte
npm install
npm run dev
```

---

## Ejercicios

1. **Fácil:** Agrega un botón "-1" que decremente el contador pero no permita valores menores a 0.
2. **Medio:** Usa `$derived` para mostrar si el contador es par o impar.
3. **Difícil:** Agrega un historial de los últimos 5 valores del contador usando un array `$state`.

---

*<- [Sección 01: Primer Componente](../01-introduccion/) · [Sección 03: Props ->](../03-props/)*
