# Semana 7 — SvelteKit 2 + Svelte 5: De los Fundamentos al Control Industrial Full-Stack

### Lenguaje de Programación Visual · Ingeniería Mecatrónica — FIUNA (2026-2)
**Profesor:** Jorge Luis Tillería Mereles  
**Auxiliar de Práctica:** Carlos María Benítez Cardozo  

> **Basado en la documentación oficial:** [svelte.dev/docs/kit](https://svelte.dev/docs/kit)

---

## 1. Introducción a SvelteKit

En la **Semana 6**, exploramos los fundamentos de **Svelte 5** como compilador de interfaces de usuario y su nuevo paradigma de reactividad basado en **Runes** (`$state`, `$derived`, `$effect`, `$props`).

En esta **Semana 7**, damos el salto al desarrollo **Full-Stack profesional con SvelteKit 2**. SvelteKit extiende las capacidades de Svelte dotándolo de:
- **Enrutamiento basado en archivos (File-based Routing):** Definición declarativa de rutas estáticas, dinámicas y rest.
- **Layouts Jerárquicos Persistentes:** Creación de UI Shells industriales que no se recargan al navegar.
- **Carga de Datos en Servidor (`load`):** Conexión protegida con bases de datos, buses de campo y drivers de hardware.
- **Mutaciones Progresivas (Form Actions + `use:enhance`):** Modificación de estado con validación en servidor y soporte de accesibilidad nativa.
- **Rutas de Servidor y Streaming:** Endpoints REST independientes y transmisión en vivo por *Server-Sent Events (SSE)*.
- **Middleware Global de Seguridad (Hooks):** Autenticación por cookies (RBAC) y encabezados de rendimiento `Server-Timing`.

```
┌─────────────────────────────────────────────────────────────────┐
│                    NAVEGADOR CLIENTE (SPA)                     │
│  Runes Svelte 5 · Hidratación · EventSource (SSE) · use:enhance │
└────────────────────────▲───────────────────▲────────────────────┘
                         │ (SSR / SSE / JSON)│ (Form Actions / POST)
┌────────────────────────┴───────────────────┴────────────────────┐
│                    SERVIDOR SVELTEKIT 2                        │
│                                                                 │
│   src/hooks.server.js ──> Interceptación global de peticiones   │
│   +page.server.js     ──> Carga de datos segura y Form Actions  │
│   +server.js          ──> Endpoints API REST y streaming SSE    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Estructura Didáctica de la Semana 7

El contenido ha sido dividido pedagógicamente en carpetas modulares que progresan desde los conceptos básicos hasta un sistema SCADA completo y avanzado:

| Sección | Directorio | Tema Central | Ejemplos Incluidos |
|---|---|---|---|
| **01** | [`01-enrutamiento-y-paginas/`](./01-enrutamiento-y-paginas/) | File-Based Routing | Rutas estáticas, dinámicas `[id]`, comodines `[...slug]` y `goto()`. |
| **02** | [`02-layouts-y-anidacion/`](./02-layouts-y-anidacion/) | Layouts y UI Shells | Snippets `{@render children()}`, sub-layouts anidados y reseteo `@`. |
| **03** | [`03-carga-de-datos-load/`](./03-carga-de-datos-load/) | Carga en Servidor | `+page.server.js`, tipado `$props()`, errores `error(404)` y `+error.svelte`. |
| **04** | [`04-form-actions-y-mutaciones/`](./04-form-actions-y-mutaciones/) | Form Actions | Mutaciones progresivas, `use:enhance`, validación con `fail()` y spinners. |
| **05** | [`05-api-endpoints-server-routes/`](./05-api-endpoints-server-routes/) | Rutas API y Streaming | Endpoints REST (`+server.js`), Server-Sent Events (SSE) y exportación CSV. |
| **06** | [`06-hooks-y-middleware/`](./06-hooks-y-middleware/) | Hooks de Servidor | `hooks.server.js`, control de acceso (RBAC), `locals` y `Server-Timing`. |
| **07** | [`07-proyecto-avanzado-dashboard/`](./07-proyecto-avanzado-dashboard/) | **Proyecto Avanzado SCADA** | **Plataforma Full-Stack ejecutable:** telemetría 1 Hz en vivo, parada de emergencia, osciloscopio reactivo SVG y control PID. |

---

## 3. Requisitos del Entorno

- **Node.js:** v18.18 o superior (v20+ recomendado)
- **npm:** v9 o superior
- **Navegador Moderno:** Chrome, Edge o Firefox con soporte SSE y Web APIs

---

## 4. Inicio Rápido: Ejecución del Proyecto Avanzado

Para ejecutar inmediatamente la aplicación full-stack de la **Sección 07**:

```bash
# 1. Entrar al directorio del proyecto avanzado
cd 07-proyecto-avanzado-dashboard

# 2. Instalar dependencias (si es necesario)
npm install

# 3. Iniciar el servidor local de desarrollo con Vite
npm run dev
```

Navega a:  
👉 **`http://localhost:5173`**

### Validar integridad de tipos y compilación:
```bash
npm run check
```

---

## 5. Metodología de Estudio Sugerida

1. **Lectura Guiada:** Comienza por el `README.md` de la **Sección 01** y avanza secuencialmente hasta la **Sección 06** para afianzar cada concepto teórico.
2. **Inspección de Código:** Analiza los componentes `.svelte` y scripts `.server.js` incluidos en cada carpeta para entender la sintaxis moderna con Runes de Svelte 5.
3. **Ejecución y Maniobra:** Inicia el proyecto avanzado de la **Sección 07** para experimentar la integración de todos los componentes en una aplicación industrial real.
4. **Ejercicios Prácticos:** Completa los retos propuestos al final de cada guía para consolidar tus habilidades.

---

*Facultad de Ingeniería · Universidad Nacional de Asunción (FIUNA)*  
*Lenguajes de Programación Visual — Ciclo 2026-2*
