# Trabajo Práctico 3 (TP3) — Diseño e Implementación de la Interfaz de Usuario Inicial y Arquitectura Gráfica

> ### ⚠️ ESTADO DEL DOCUMENTO: BORRADOR PRELIMINAR (EN REVISIÓN)
> Este documento representa un **borrador orientativo** para facilitar la planificación temprana de los grupos de trabajo. La versión oficial, rúbrica detallada y fecha exacta de entrega serán ratificadas y publicadas formalmente al inicio de la **Semana 8**, tras la conclusión del Primer Examen Parcial.

---

### Lenguajes de Programación Visual (Código: 5728)
**Ingeniería Mecatrónica — Facultad de Ingeniería, Universidad Nacional de Asunción (FIUNA)**  
**Primer Ciclo 2026**  
**Profesor Titular:** Ing. Jorge Luis Tillería Mereles  
**Auxiliar de Práctica:** Ing. Carlos María Benítez Cardozo  

---

## Información Preliminar del Trabajo Práctico

| Parámetro | Detalle (Sujeto a confirmación) |
|---|---|
| **Ponderación** | 5 puntos del proceso acumulado |
| **Periodo Tentativo** | Semana 8 (01/10) a Semana 10 (15/10) |
| **Fecha Límite Estimada** | Semana 10 (Tiempo Real Administrativo vs. Tiempo Real Físico) |
| **Modalidad** | Grupal (continuación del proyecto final) |
| **Tecnología Recomendada** | Svelte 5 + SvelteKit 2 (o framework web moderno afín) |

---

## Requerimientos Previstos (Borrador)

Para la entrega del TP3 se proyecta requerir:
1. **Diseño e implementación de la arquitectura gráfica base** del proyecto mecatrónico elegido en el foro.
2. **Conexión e integración con los servicios backend** desarrollados en los trabajos anteriores:
   - Consumo de la API de datos y scraping de **TP1**.
   - Integración de la interfaz conversacional con el Bot de IA de **TP2**.
3. **Desarrollo de componentes modulares y dashboards interactivos** con visualización reactiva de información.
4. **Diseño responsivo y experiencia de usuario (UX/UI)** adaptada a entornos de monitoreo y supervisión industrial.

---

## 1. Lineamientos Previstos de la Arquitectura Gráfica

### 1.1 Estructura Frontend con SvelteKit
- Implementación de navegación mediante *File-Based Routing* (`src/routes/`).
- Creación de un **Layout principal persistente** (`+layout.svelte`) que proporcione la barra de navegación (*Navbar*), panel de estado de conexión y pie de página institucional.
- Adopción del nuevo paradigma de reactividad de **Svelte 5 (Runes)**:
  - `$state` para el manejo de estados de la interfaz.
  - `$derived` para cálculos de métricas y transformaciones en tiempo real.
  - `$effect` para sincronización con endpoints de streaming o polling.

### 1.2 Integración con los Backends (TP1 y TP2)
- **Consumo de Datos (TP1):**
  - Carga eficiente de datos del backend mediante funciones `load` (`+page.server.js` o `+page.js`).
  - Tabla o tarjetas interactivas con filtros de búsqueda y ordenamiento reactivo.
- **Módulo de Asistente / Bot de IA (TP2):**
  - Componente de ventana de chat interactiva que consuma los endpoints de `/api/chat`.
  - Burbujas de diálogo diferenciadas (usuario vs asistente), indicadores de escritura (*typing indicator*) y manejo de errores ante caídas de red.

### 1.3 Estética y Experiencia de Usuario (UI/UX)
- Paleta de colores sobria, moderna y contrastada (modo oscuro técnico recomendado para consolas de supervisión).
- Tipografía moderna (inter, roboto o fuentes de ancho fijo para valores numéricos y telemetría).
- Micro-animaciones sutiles y transiciones fluidas sin sobrecargar el rendimiento de la aplicación.

---

## 2. Estructura Tentativa de la Solución

```
tp3-interfaz-grafica/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── ChatBot.svelte        <- Ventana interactiva del Bot de IA (TP2)
│   │   │   ├── DataGrid.svelte       <- Visualizador de datos extraídos (TP1)
│   │   │   ├── Navbar.svelte         <- Barra de navegación superior
│   │   │   └── MetricCard.svelte     <- Tarjetas de indicadores mecatrónicos
│   │   └── api/
│   │       ├── client_tp1.js         <- Cliente HTTP para consumir API de TP1
│   │       └── client_tp2.js         <- Cliente HTTP para el Bot de IA de TP2
│   └── routes/
│       ├── +layout.svelte            <- Shell general de la aplicación
│       ├── +page.svelte              <- Vista principal del dashboard
│       ├── datos/
│       │   └── +page.svelte          <- Explorador de datos de TP1
│       └── asistente/
│           └── +page.svelte          <- Centro de interacción con el Bot
├── package.json
└── README.md
```

---

## 3. Próximos Pasos para los Estudiantes

1. Enfocar los esfuerzos inmediatos en el cierre y consolidación del **TP1** y **TP2**, así como la preparación para el **1er Examen Parcial**.
2. Revisar los conceptos de frontend introducidos en las ramas didácticas `semana-6` (Svelte 5) y `semana-7` (SvelteKit 2).
3. Aguardar la publicación formal de la rúbrica y directivas finales al inicio de la Semana 8.
