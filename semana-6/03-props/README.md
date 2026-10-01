# Sección 03 — Props: Comunicación entre Componentes

> 📖 Referencia:
> - [svelte.dev/tutorial/svelte/declaring-props](https://svelte.dev/tutorial/svelte/declaring-props)
> - [svelte.dev/tutorial/svelte/default-values](https://svelte.dev/tutorial/svelte/default-values)
> - [svelte.dev/tutorial/svelte/spread-props](https://svelte.dev/tutorial/svelte/spread-props)

---

## 3.1 ¿Qué son las Props?

Las **props** (propiedades) son la forma en que un componente padre **pasa datos** a un componente hijo. Son la base de la composición de componentes.

```
App.svelte (padre)
│
│  <Tarjeta titulo="Hola" color="blue" />
│         ↓ pasa datos
│
└── Tarjeta.svelte (hijo)
       recibe: { titulo, color }
```

---

## 3.2 Declarando Props con `$props()`

En Svelte 5, las props se declaran con la rune `$props()`:

```svelte
<!-- Hijo.svelte -->
<script>
  // Desestructuramos las props que esperamos recibir
  let { nombre, edad } = $props();
</script>

<p>{nombre} tiene {edad} años</p>
```

```svelte
<!-- Padre (App.svelte) -->
<script>
  import Hijo from './Hijo.svelte';
</script>

<Hijo nombre="Carlos" edad={23} />
```

---

## 3.3 Valores por Defecto

Puedes definir valores por defecto directamente en la desestructuración:

```svelte
<!-- Tarjeta.svelte -->
<script>
  let {
    titulo = "Sin título",
    descripcion = "Sin descripción",
    color = "#4f46e5",
    activa = false
  } = $props();
</script>

<div class="tarjeta" style="border-color: {color}">
  <h2>{titulo}</h2>
  <p>{descripcion}</p>
  {#if activa}
    <span class="badge">✓ Activa</span>
  {/if}
</div>
```

```svelte
<!-- App.svelte -->
<!-- Sin pasar props → usa valores por defecto -->
<Tarjeta />

<!-- Pasando algunas props -->
<Tarjeta titulo="Robótica" color="#10b981" activa />

<!-- Pasando todas las props -->
<Tarjeta titulo="IA" descripcion="Machine Learning" color="#f59e0b" activa={false} />
```

---

## 3.4 Spread Props — Pasar Múltiples Props a la Vez

Cuando tienes un objeto con las props, puedes "esparcirlo" con `{...objeto}`:

```svelte
<script>
  import Tarjeta from './Tarjeta.svelte';

  let datos = {
    titulo: "Mecatrónica",
    descripcion: "Integración de sistemas",
    color: "#8b5cf6",
    activa: true
  };
</script>

<!-- Sin spread (verboso): -->
<Tarjeta titulo={datos.titulo} descripcion={datos.descripcion} ... />

<!-- Con spread (limpio): -->
<Tarjeta {...datos} />
```

---

## 3.5 Props de Solo Lectura vs Enlazables

Por defecto, las props son **de solo lectura** desde el hijo. Si el padre quiere que el hijo pueda modificar una prop, debe usar `bind:`:

```svelte
<!-- Padre -->
<script>
  let volumen = $state(50);
</script>
<Slider bind:valor={volumen} />
<p>Volumen actual: {volumen}</p>
```

```svelte
<!-- Slider.svelte (hijo) -->
<script>
  let { valor = $bindable(50) } = $props();
</script>
<input type="range" bind:value={valor} min="0" max="100" />
```

> 💡 `$bindable()` marca una prop como enlazable en ambas direcciones.

---

## 3.6 Flujo de Datos: Unidireccional

```
Padre → (props) → Hijo        [siempre permitido]
Hijo  → (bind:) → Padre       [requiere $bindable]
Hijo  → (eventos) → Padre     [patrón alternativo]
```

El flujo unidireccional hace el código más **predecible y fácil de depurar**.

---

## 🧪 Mini Página: Galería de Tarjetas

Muestra una galería de tarjetas de proyectos, donde cada tarjeta es un componente que recibe props.

**Archivos:**
- [`App.svelte`](./App.svelte) — Componente raíz con lista de proyectos
- [`TarjetaProyecto.svelte`](./TarjetaProyecto.svelte) — Componente reutilizable

---

## ✏️ Ejercicios

1. **Fácil:** Agrega una prop `icono` (emoji) a `TarjetaProyecto.svelte` con valor por defecto "📁".
2. **Medio:** Agrega una prop `etiquetas` que sea un array de strings y muéstralos como badges.
3. **Difícil:** Crea un componente `Galeria.svelte` que reciba un array de objetos y renderice múltiples `TarjetaProyecto` con spread props.

---

*← [Sección 02: Reactividad](../02-reactividad/) · [Sección 04: Lógica →](../04-logica/)*
