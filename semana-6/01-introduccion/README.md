# Sección 01 — Tu Primer Componente y Atributos Dinámicos

> 📖 Referencia: [svelte.dev/tutorial/svelte/your-first-component](https://svelte.dev/tutorial/svelte/your-first-component)

---

## 1.1 ¿Qué es un Componente en Svelte?

Un **componente** es la unidad básica de construcción en Svelte. Es un archivo con extensión `.svelte` que combina:

- **HTML** → estructura visual
- **JavaScript** → lógica y datos
- **CSS** → estilos encapsulados

Piensa en un componente como un **bloque reutilizable** de interfaz, similar a una pieza de LEGO.

```
App.svelte         ← Componente raíz
├── Header.svelte  ← Componente hijo
├── Card.svelte    ← Componente reutilizable
└── Footer.svelte  ← Componente hijo
```

---

## 1.2 Tu Primer Componente

El componente más simple que puedes crear:

```svelte
<!-- App.svelte -->
<h1>¡Hola, Svelte!</h1>
```

Esto es HTML puro y válido. En Svelte, **todo HTML es válido dentro del template**.

---

## 1.3 Interpolación de Expresiones `{}`

Para mostrar valores dinámicos en el HTML, usamos llaves `{}`:

```svelte
<script>
  let nombre = "Mecatrónica";
  let año = 2026;
</script>

<h1>Bienvenido a {nombre}</h1>
<p>Año académico: {año}</p>
<p>El doble del año es: {año * 2}</p>
```

> 💡 Dentro de `{}` puedes poner **cualquier expresión JavaScript** válida.

---

## 1.4 Atributos Dinámicos

También puedes usar `{}` para establecer atributos HTML de forma dinámica:

```svelte
<script>
  let src = "https://picsum.photos/200";
  let nombre = "Carlos";
  let activo = true;
</script>

<!-- Atributo dinámico -->
<img {src} alt="Foto de {nombre}" />

<!-- Shorthand: cuando variable y atributo tienen el mismo nombre -->
<img {src} alt="avatar" />
<!-- equivale a: <img src={src} alt="avatar" /> -->

<!-- Atributo booleano -->
<button disabled={!activo}>Enviar</button>
```

---

## 1.5 Estilos con Alcance (Scoped CSS)

Los estilos en Svelte son automáticamente **scoped**: solo afectan al componente donde están definidos.

```svelte
<p>Este párrafo es rojo (solo en este componente)</p>

<style>
  p {
    color: red;  /* NO afecta a otros componentes */
    font-weight: bold;
  }
</style>
```

---

## 1.6 Componentes Anidados

Puedes importar y usar otros componentes como si fueran etiquetas HTML:

```svelte
<!-- Perfil.svelte -->
<script>
  import Avatar from './Avatar.svelte';
</script>

<div class="perfil">
  <Avatar />
  <h2>Carlos Benitez</h2>
</div>
```

> ⚠️ Los componentes siempre empiezan con **mayúscula** (`<Avatar />`) para distinguirlos de los elementos HTML nativos.

---

## 1.7 HTML Dinámico con `{@html}`

Para renderizar HTML crudo (con precaución):

```svelte
<script>
  let contenido = "<strong>Texto en negrita</strong> con <em>énfasis</em>";
</script>

<p>{@html contenido}</p>
```

> ⚠️ **Advertencia de seguridad:** Solo usa `{@html}` con contenido de confianza. Nunca con datos del usuario (riesgo de XSS).

---

## 🧪 Mini Página: Tarjeta de Perfil

Este ejemplo combina todos los conceptos anteriores en una tarjeta de perfil interactiva.

**Archivos:**
- [`App.svelte`](./App.svelte) — Componente raíz
- [`TarjetaPerfil.svelte`](./TarjetaPerfil.svelte) — Componente de tarjeta

**Para ejecutar:**
```bash
npm create vite@latest semana6-01 -- --template svelte
cd semana6-01
# Reemplaza el contenido de src/App.svelte con el código de App.svelte
npm install
npm run dev
```

---

## ✏️ Ejercicios

1. **Fácil:** Cambia el nombre y la descripción en `TarjetaPerfil.svelte` con tus propios datos.
2. **Medio:** Agrega una propiedad `hobbies` como lista de strings y muéstralos en la tarjeta.
3. **Difícil:** Crea un componente `Badge.svelte` que reciba un texto y un color, y úsalo dentro de `TarjetaPerfil.svelte` para mostrar etiquetas de habilidades.

---

*← [README principal](../README.md) · [Sección 02: Reactividad →](../02-reactividad/)*
