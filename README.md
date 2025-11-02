# 🧠 Thinking Patterns — OOP for Thought Design

> “Cuando aprendes a modular código, aprendes a modular pensamientos.”

Una colección de **metapatrones**: cómo las prácticas de ingeniería enseñan a pensar.
Cada clase, patrón y docstring conecta una habilidad técnica con una cognitiva.

## 🚀 Objetivos
- Traducir **patrones de diseño** en **patrones de pensamiento**.
- Crear una **biblioteca modular** de aforismos y hábitos mentales.
- Conectar **código, docstring y reflexión**.

## 🗺️ Estructura
```
thinking-patterns/
├── src/thinking_patterns/core/        # Clases base y catálogo
├── src/thinking_patterns/examples/    # Ejemplos ejecutables
├── notebooks/                         # Demos interactivos
├── wiki/                              # Páginas base para la Wiki
├── .github/workflows/                 # CI (lint + pruebas mínimas)
├── tools/                             # Utilidades opcionales
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── requirements.txt
```

## 🧩 Ejemplo mínimo
```python
from thinking_patterns.core.idea_pattern import IdeaPattern
from thinking_patterns.core.patterns_catalog import LoggingComoNarrativa

patron = LoggingComoNarrativa()
print(patron.aplicar({"paso": "feature_engineering", "decision": "descartar outliers 99p"}))
```

## 🌐 Wiki Pages sugeridas
- 01_intro.md — Filosofía y motivación
- 02_metapatterns_catalog.md — Catálogo de patrones ↔ habilidades cognitivas
- 03_aforismos_coleccion.md — Frases concisas
- 04_frameworks_de_pensamiento.md — UML/PlantUML y mapas mentales
- 05_casos_de_uso.md — Docencia, coaching, BI

> Recomendación: crea la Wiki del repo y copia/pega estos archivos para iniciar.

## ▶️ Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
python -m pip install -e .
python src/thinking_patterns/examples/logging_narrativa.py
```

## 🪄 Roadmap corto
- [ ] CLI para generar aforismos desde plantillas
- [ ] Export a Wiki automático
- [ ] Diagrama PlantUML de relaciones de clases
- [ ] Tests de regresión sobre frases generadas

---

**Licencia:** MIT
