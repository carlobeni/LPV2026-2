# Sección 06 — Bindings Bidireccionales

> Referencia:
> - [svelte.dev/tutorial/svelte/text-inputs](https://svelte.dev/tutorial/svelte/text-inputs)
> - [svelte.dev/tutorial/svelte/numeric-inputs](https://svelte.dev/tutorial/svelte/numeric-inputs)
> - [svelte.dev/tutorial/svelte/checkbox-inputs](https://svelte.dev/tutorial/svelte/checkbox-inputs)
> - [svelte.dev/tutorial/svelte/select-bindings](https://svelte.dev/tutorial/svelte/select-bindings)

---

## 6.1 Qué es un Binding

Un **binding** es una conexión bidireccional entre un elemento del DOM y una variable de Svelte.

Sin binding (manual):
```svelte
<script>
  let nombre = $state("");

  function actualizar(e) {
    nombre = e.target.value;  // Actualizar variable cuando el input cambia
  }
</script>

<input value={nombre} oninput={actualizar} />
<!-- nombre -> input: value={nombre}  -->
<!-- input -> nombre: oninput={actualizar}  -->
```

Con `bind:` (bidireccional y automático):
```svelte
<script>
  let nombre = $state("");
</script>

<input bind:value={nombre} />
<!-- Svelte maneja automáticamente ambas direcciones -->
```

---

## 6.2 `bind:value` — Inputs de Texto

```svelte
<script>
  let nombre = $state("");
  let comentario = $state("");
</script>

<!-- Input de texto -->
<input type="text" bind:value={nombre} placeholder="Nombre..." />

<!-- Textarea -->
<textarea bind:value={comentario} rows="4"></textarea>

<!-- La variable se actualiza en tiempo real -->
<p>Hola, {nombre || "desconocido"}!</p>
```

---

## 6.3 `bind:value` — Inputs Numéricos

Svelte convierte automáticamente el valor a número:

```svelte
<script>
  let edad = $state(18);        // number
  let temperatura = $state(25.5); // float
</script>

<input type="number" bind:value={edad} min="0" max="120" />
<input type="range" bind:value={temperatura} min="0" max="100" step="0.5" />

<p>Edad: {edad} (tipo: {typeof edad})</p>         <!-- "number" -->
<p>Temperatura: {temperatura.toFixed(1)} grados</p>
```

---

## 6.4 `bind:checked` — Checkboxes

```svelte
<script>
  let suscrito = $state(false);
  let opciones = $state(["html", "css"]);
</script>

<!-- Checkbox simple -->
<input type="checkbox" bind:checked={suscrito} id="suscripcion" />
<label for="suscripcion">Suscribirse al newsletter</label>

<!-- Grupo de checkboxes con bind:group -->
<input type="checkbox" bind:group={opciones} value="html" /> HTML
<input type="checkbox" bind:group={opciones} value="css" />  CSS
<input type="checkbox" bind:group={opciones} value="js" />   JavaScript
<p>Seleccionados: {opciones.join(", ")}</p>
```

---

## 6.5 `bind:value` — Selects

```svelte
<script>
  let color = $state("azul");
  let colores = ["rojo", "verde", "azul", "morado"];
</script>

<select bind:value={color}>
  {#each colores as c}
    <option value={c}>{c}</option>
  {/each}
</select>

<p style="color: {color}">Texto de color {color}</p>
```

---

## 6.6 Tabla Resumen de Bindings

| Tipo de input | Directiva | Variable resultante |
|---------------|-----------|---------------------|
| `<input type="text">` | `bind:value` | `string` |
| `<input type="number">` | `bind:value` | `number` |
| `<input type="range">` | `bind:value` | `number` |
| `<input type="checkbox">` | `bind:checked` | `boolean` |
| `<input type="checkbox">` (grupo) | `bind:group` | `string[]` |
| `<input type="radio">` | `bind:group` | `string` |
| `<select>` | `bind:value` | `string` |
| `<textarea>` | `bind:value` | `string` |

---

## Mini Página: Editor de Texto en Vivo

Un editor con vista previa en tiempo real que demuestra múltiples tipos de binding.

**Archivo:** [`App.svelte`](./App.svelte)

---

## Ejercicios

1. **Fácil:** Agrega un slider para controlar el tamaño de fuente del preview.
2. **Medio:** Agrega checkboxes para aplicar negrita, cursiva y subrayado al texto.
3. **Difícil:** Implementa un historial de deshacer/rehacer con Ctrl+Z.

---

*<- [Sección 05: Eventos](../05-eventos/) · [Sección 07: Estilos ->](../07-estilos/)*
