# Trabajos Prácticos (TPs) — Lenguajes de Programación Visual

### Carrera: Ingeniería Mecatrónica · Facultad de Ingeniería — Universidad Nacional de Asunción (FIUNA)
**Primer Ciclo 2026 (Optativa - Código: 5728)**  
**Profesor Titular:** Ing. Jorge Luis Tillería Mereles  
**Auxiliar de Práctica:** Ing. Carlos María Benítez Cardozo  

---

## 1. Visión General de los Trabajos Prácticos

En esta rama (`TPs`) se centralizan las especificaciones, alcances técnicos y rúbricas de evaluación correspondientes a los **tres Trabajos Prácticos** del semestre.

Los trabajos prácticos están diseñados de forma incremental y acumulativa, convergiendo en el desarrollo del **Proyecto Final de la Cátedra**:

```
┌──────────────────────────────────────────────────────────────┐
│  TP1: Extracción de Datos + Base de Datos + FastAPI REST    │
│  (Semanas 1 a 4 · 5 Puntos)                                  │
└──────────────────────────────┬───────────────────────────────┘
                               │ alimenta
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  TP2: Bot de Inteligencia Artificial accesible vía API      │
│  (Semanas 5 a 7 · 5 Puntos · Sin interfaz gráfica)           │
└──────────────────────────────┬───────────────────────────────┘
                               │ se integra en
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  TP3: Interfaz de Usuario y Arquitectura Gráfica (Frontend)  │
│  (Semanas 8 a 10 · 5 Puntos · [BORRADOR PRELIMINAR])         │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. Índice de Trabajos Prácticos

| TP | Directorio | Alcance Principal | Ponderación | Estado |
|:---:|---|---|:---:|:---:|
| **TP 1** | [`TP1/`](./TP1/README.md) | **Web Scraping y API REST Propia:** Extracción de datos de fuentes web/APIs, guardado en base de datos relacional y disponibilización de endpoints en FastAPI con Pydantic v2. | **5 pts** | **OFICIAL** |
| **TP 2** | [`TP2/`](./TP2/README.md) | **Bot de IA Accesible por API:** Agente inteligente / LLM integrado a backend FastAPI, persistencia de conversaciones/memoria en base de datos. Sin frontend obligatorio. | **5 pts** | **OFICIAL** |
| **TP 3** | [`TP3/`](./TP3/README.md) | **Diseño de Interfaz de Usuario y Arquitectura Gráfica:** Estructura gráfica base en SvelteKit, componentes reactivos e integración con los backends de TP1 y TP2. | **5 pts** | **BORRADOR** |

---

## 3. Requerimientos Resumidos por Trabajo Práctico

### [Trabajo Práctico 1 (TP1)](./TP1/README.md)
Para la entrega se requiere:
1. Extracción de datos a través de scraping de datos o consumo de una API
2. Guardado de la información en una base de datos
3. Disponibilización de la manipulación de la información a través de una API propia desarrollada en FastAPI

> *El lugar de extracción de datos se definirá según el proyecto final elegido en el foro.*

---

### [Trabajo Práctico 2 (TP2)](./TP2/README.md)
Para la entrega se requiere:
1. Creación de un Bot de Inteligencia Artificial accesible mediante API backend
2. Integración de lógica de inferencia, procesamiento de lenguaje natural o agentes inteligentes (vía LLMs, APIs de IA, o modelos locales)
3. Persistencia de contexto, conversaciones o base de conocimiento en una base de datos
4. Disponibilización e interacción con el bot a través de una API propia desarrollada en FastAPI (sin interfaz gráfica obligatoria)

> *El dominio temático del bot de IA se definirá según el proyecto final elegido en el foro.*

---

### [Trabajo Práctico 3 (TP3) — Borrador](./TP3/README.md)
Diseño e implementación de la interfaz de usuario inicial y arquitectura gráfica:
1. Arquitectura gráfica base y sistema de diseño en frontend moderno (SvelteKit 2 + Svelte 5).
2. Conexión e integración con los servicios backend de TP1 y TP2.
3. Dashboards interactivos y componentes reactivos de visualización.

> *Nota: Este documento es un borrador orientativo sujeto a ratificación al inicio de la Semana 8 tras el Primer Parcial.*

---

*Facultad de Ingeniería · Universidad Nacional de Asunción (FIUNA)*  
*Lenguajes de Programación Visual — Ciclo 2026-2*
