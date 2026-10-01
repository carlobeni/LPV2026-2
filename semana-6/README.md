## Semana 6 — Introducción a Svelte 5
### Lenguaje de Programación Visual · Ingeniería Mecatrónica - FIUNA

> **Basado en:** [svelte.dev/tutorial](https://svelte.dev/tutorial)

---

## ¿Qué es Svelte?

**Svelte** es un framework de JavaScript para construir interfaces de usuario. A diferencia de React o Vue, Svelte **compila** el código en JavaScript vanilla optimizado durante la construcción, eliminando la sobrecarga del DOM virtual en tiempo de ejecución.

```
Tu código .svelte  →  Compilador Svelte  →  JS puro + HTML + CSS optimizados
```

### Ventajas clave frente a otros frameworks

| Característica        | React / Vue          | Svelte               |
|-----------------------|----------------------|----------------------|
| DOM Virtual           | ✅ Sí (overhead)    | ❌ No necesita       |
| Tamaño del bundle     | ~40-100 KB           | ~2-10 KB             |
| Reactividad           | Hooks / Options API  | Nativa con `$state`  |
| Curva de aprendizaje  | Media-Alta           | Baja                 |
| Sintaxis              | JSX / Template       | HTML + JS directo    |

---

## Requisitos Previos

- Node.js v18 o superior
- npm v9 o superior
- Conocimientos básicos de HTML, CSS y JavaScript

---

## Estructura de esta Guía

| Sección | Tema | Mini Página |
|---------|------|-------------|
| [01](./01-introduccion/) | Primer Componente & Atributos Dinámicos | Tarjeta de perfil |
| [02](./02-reactividad/) | Estado Reactivo con `$state` | Contador interactivo |
| [03](./03-props/) | Props y comunicación entre componentes | Galería de tarjetas |
| [04](./04-logica/) | Bloques `{#if}`, `{#each}`, `{#await}` | Dashboard de lista |
| [05](./05-eventos/) | Eventos DOM y manejadores | Formulario de contacto |
| [06](./06-bindings/) | Bindings bidireccionales | Editor de texto en vivo |
| [07](./07-estilos/) | Clases dinámicas y estilos reactivos | Tema claro/oscuro |
| [08](./08-transiciones/) | Transiciones y animaciones | Lista animada |

---

## Configuración del Proyecto

### Opción A — Proyecto nuevo con `sv create` (Recomendado)

```bash
# Crear un nuevo proyecto SvelteKit
npx sv create mi-app-svelte
cd mi-app-svelte
npm install
npm run dev
```

### Opción B — Svelte puro con Vite

```bash
# Crear proyecto Svelte sin SvelteKit
npm create vite@latest mi-app -- --template svelte
cd mi-app
npm install
npm run dev
```

### Opción C — Playground Online

Puedes practicar sin instalar nada en:
👉 **[svelte.dev/playground](https://svelte.dev/playground)**

---

## Anatomía de un Componente `.svelte`

Todo componente Svelte tiene hasta tres secciones:

```svelte
<!-- 1. SCRIPT: lógica JavaScript -->
<script>
  let nombre = $state("Mundo");
</script>

<!-- 2. TEMPLATE: marcado HTML con expresiones -->
<h1>Hola, {nombre}!</h1>
<input bind:value={nombre} />

<!-- 3. STYLE: CSS con alcance al componente -->
<style>
  h1 {
    color: rebeccapurple;
    font-family: sans-serif;
  }
</style>
```

> 💡 El `<style>` en Svelte es **scoped** por defecto: los estilos solo afectan al componente actual.

---

## Cómo Usar esta Guía

1. Lee la explicación teórica de cada sección
2. Estudia el código del ejemplo
3. Ejecuta la mini página en tu navegador
4. Completa los ejercicios propuestos al final de cada sección
5. Avanza a la siguiente sección

---

*Semana 6 · LPV 2026-2 · FIUNA*
