# Sección 07 — Proyecto Avanzado: Plataforma de Telemetría y Control SCADA en Tiempo Real

> **Aplicación Full-Stack Completa con SvelteKit 2 + Svelte 5 (Runes Mode)**  
> **Facultad de Ingeniería — Universidad Nacional de Asunción (FIUNA)**  
> *Lenguajes de Programación Visual 2026-2*

---

## 7.1 Visión General del Proyecto

Esta carpeta contiene la **culminación avanzada** de la guía de SvelteKit: un sistema industrial real de monitoreo y telemetría diseñado bajo especificaciones de ingeniería mecatrónica.

Integra en una sola solución funcional todos los pilares estudiados en las secciones 01 a 06:
1. **Enrutamiento y Layouts Jerárquicos** (`+layout.svelte`, `{@render children()}`).
2. **Carga en Servidor y Estado Inicial Hidratado** (`+page.server.js`).
3. **Mutaciones con Form Actions Progresivas** (`use:enhance`, validación en servidor, parada de emergencia).
4. **Streaming en Vivo vía Server-Sent Events (SSE)** con `ReadableStream` (`/api/telemetria/stream`).
5. **Generación al Vuelo de Descarga CSV de Auditoría** (`/api/exportar`).
6. **Middleware Global de Seguridad y Trazabilidad** (`src/hooks.server.js` con RBAC y `Server-Timing`).
7. **Visualización Gráfica Reactiva en SVG Puro con Runes de Svelte 5** (`$state`, `$derived`, `$effect`).

---

## 7.2 Arquitectura del Sistema

```
07-proyecto-avanzado-dashboard/
├── package.json                   <- SvelteKit 2, Svelte 5.57+, Vite 8
├── vite.config.js                 <- Configuración de Vite con modo Runes forzado
├── src/
│   ├── app.d.ts                   <- Tipado de App.Locals (sesión y roles)
│   ├── app.html                   <- Plantilla HTML con preloading
│   ├── hooks.server.js            <- Middleware global (auth, Server-Timing)
│   └── routes/
│       ├── +layout.server.js      <- Carga global de sesión
│       ├── +layout.svelte         <- UI Shell industrial, Navbar y Footer
│       ├── +page.server.js        <- Form Actions (Parada, Setpoint, Actuadores)
│       ├── +page.svelte           <- Dashboard en vivo con Osciloscopio SVG
│       ├── about/
│       │   └── +page.svelte       <- Especificación técnica de arquitectura
│       └── api/
│           ├── telemetria/
│           │   └── stream/+server.js <- Streaming SSE continuo (1 Hz)
│           └── exportar/
│               └── +server.js        <- Exportación directa de auditoría en CSV
```

---

## 7.3 Instrucciones de Ejecución Inmediata

Este proyecto cuenta con sus dependencias instaladas y configuradas. Para iniciarlo:

```bash
# 1. Posicionarse en el directorio del proyecto avanzado
cd 07-proyecto-avanzado-dashboard

# 2. Iniciar el servidor local de desarrollo
npm run dev
```

Abre en tu navegador la URL:
👉 **`http://localhost:5173`**

### Verificación de Tipos y Diagnósticos:
```bash
npm run check
```

---

## 7.4 Características Técnicas Destacadas

### 1. Osciloscopio Reactivo en SVG Puro (Sin Dependencias Externas)
El gráfico temporal calcula sus puntos poligonales de forma reactiva mediante `$derived.by()` a partir de un búfer circular de 25 muestras en `$state`:
- **Curva Roja:** Temperatura (°C) con línea de advertencia crítica a 95°C.
- **Curva Azul:** Presión de colector (bar x 10).
- **Rendimiento:** Cero recargas de DOM, aprovechando la reactividad fina (*fine-grained*) de Svelte 5 sin Virtual DOM.

### 2. Parada de Emergencia y Enclavamiento Físico
Al presionar el botón de **PARADA DE EMERGENCIA**:
- La acción de servidor desconecta inmediatamente todos los actuadores principales.
- Abre la válvula de alivio de presión por enclavamiento de seguridad.
- La interfaz activa un banner de advertencia visual y bloquea maniobras individuales hasta que un operador presione **REARMAR PLANTA**.

### 3. Progressive Enhancement (`use:enhance`)
El ajuste del Setpoint de Presión y la alternancia de bombas se envían mediante formularios estándar HTML con `use:enhance`. Los datos se validan en el servidor y la interfaz actualiza los estados de forma optimista con retroalimentación visual inmediata.

---

## 7.5 Preguntas de Autoevaluación para el Estudiante

1. **¿Por qué se eligió Server-Sent Events (SSE) en lugar de WebSockets para este dashboard?**  
   *Pista:* Considera la unidireccionalidad de las lecturas físicas, la reconexión nativa del navegador y la compatibilidad con cortafuegos HTTP.
2. **¿Qué ventaja proporciona `Server-Timing` inyectado en `hooks.server.js` al depurar sistemas mecatrónicos en planta?**
3. **¿Cómo garantiza Svelte 5 que el gráfico SVG no vuelva a renderizar toda la página cuando llega un nuevo paquete SSE cada segundo?**

---

*<- [Sección 06: Hooks y Middleware](../06-hooks-y-middleware/) · [README Principal del Curso](../README.md)*
