# Sección 04 — Lógica en el Template: `{#if}`, `{#each}`, `{#await}`

> 📖 Referencia:
> - [svelte.dev/tutorial/svelte/if-blocks](https://svelte.dev/tutorial/svelte/if-blocks)
> - [svelte.dev/tutorial/svelte/each-blocks](https://svelte.dev/tutorial/svelte/each-blocks)
> - [svelte.dev/tutorial/svelte/await-blocks](https://svelte.dev/tutorial/svelte/await-blocks)

---

## 4.1 Bloque `{#if}` — Renderizado Condicional

Muestra elementos solo si se cumple una condición:

```svelte
<script>
  let usuario = $state(null);
  let cargando = $state(false);
</script>

{#if cargando}
  <p>Cargando...</p>
{:else if usuario}
  <h2>Bienvenido, {usuario.nombre}!</h2>
{:else}
  <p>Por favor inicia sesión.</p>
{/if}
```

### Estructura completa de `{#if}`:
```
{#if condicion}
  ...se renderiza si condicion es verdadera...
{:else if otraCondicion}
  ...se renderiza si otraCondicion es verdadera...
{:else}
  ...se renderiza si ninguna condición es verdadera...
{/if}
```

---

## 4.2 Bloque `{#each}` — Iteración sobre Listas

Para renderizar una lista de elementos:

```svelte
<script>
  let frutas = $state(["manzana", "banana", "naranja"]);
</script>

<ul>
  {#each frutas as fruta}
    <li>{fruta}</li>
  {/each}
</ul>
```

### Con índice:
```svelte
{#each frutas as fruta, indice}
  <li>{indice + 1}. {fruta}</li>
{/each}
```

### Con bloque vacío (`{:else}`):
```svelte
{#each lista as item}
  <li>{item}</li>
{:else}
  <p>La lista está vacía.</p>
{/each}
```

### `{#each}` con key para actualizaciones eficientes:
```svelte
<!-- La key ayuda a Svelte a identificar qué elemento cambió -->
{#each usuarios as usuario (usuario.id)}
  <Fila nombre={usuario.nombre} />
{/each}
```

> 💡 Siempre usa una key única cuando el orden de la lista puede cambiar. Sin key, Svelte podría reutilizar el DOM de forma incorrecta.

---

## 4.3 Bloque `{#await}` — Manejo de Promesas

Para manejar operaciones asíncronas (como llamadas a APIs):

```svelte
<script>
  async function obtenerDatos() {
    const res = await fetch("https://api.ejemplo.com/datos");
    if (!res.ok) throw new Error("Error al cargar");
    return res.json();
  }

  let promesa = $state(obtenerDatos());
</script>

{#await promesa}
  <!-- Estado: cargando -->
  <p>⏳ Cargando datos...</p>

{:then datos}
  <!-- Estado: resuelto exitosamente -->
  {#each datos as item}
    <p>{item.nombre}</p>
  {/each}

{:catch error}
  <!-- Estado: error -->
  <p>❌ Error: {error.message}</p>
{/await}
```

### Forma corta (solo éxito):
```svelte
{#await promesa then datos}
  <p>{datos.nombre}</p>
{/await}
```

---

## 4.4 Comparación Visual de los Bloques

```
Svelte Template Logic:

{#if condicion}        → Solo renderiza si condicion = true
{:else if otra}        → Alternativa condicional
{:else}                → Caso por defecto
{/if}

{#each array as item}  → Itera sobre un array
{:else}                → Cuando el array está vacío
{/each}

{#await promesa}       → Estado de carga
{:then resultado}      → Promesa resuelta
{:catch error}         → Promesa rechazada
{/await}
```

---

## 🧪 Mini Página: Dashboard de Tareas

Un panel de gestión de tareas que combina `{#if}`, `{#each}` y `{#await}`.

**Archivos:**
- [`App.svelte`](./App.svelte) — Dashboard completo

---

## ✏️ Ejercicios

1. **Fácil:** Agrega un filtro para mostrar solo las tareas completadas o solo las pendientes.
2. **Medio:** Implementa la capacidad de editar el texto de una tarea existente.
3. **Difícil:** Agrega paginación para mostrar de a 5 tareas por página.

---

*← [Sección 03: Props](../03-props/) · [Sección 05: Eventos →](../05-eventos/)*
