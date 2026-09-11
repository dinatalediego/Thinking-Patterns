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


## 🧭 Decision Compiler v0.2

Thinking Patterns ahora también puede funcionar como una capa determinística de **Decision Intelligence**.

`DecisionCompiler` recibe una decisión estructurada y la compila en un paquete auditable con:

- evidencia explícita y calidad de fuente;
- supuestos con falsificadores;
- alternativas comparables y opción seleccionada;
- resultado esperado, métrica y fecha de revisión;
- reversibilidad y trigger de rollback;
- `readiness_score`, veredicto y hallazgos adversariales.

Ejemplo:

```python
from thinking_patterns.core.decision_compiler import (
    DecisionCase, Evidence, Option, compile_decision
)

case = DecisionCase(
    decision_id="demo",
    question="¿Cambiar la política?",
    options=(
        Option(id="hold", title="Mantener"),
        Option(id="change", title="Cambiar", evidence_ids=("e1",)),
    ),
    selected_option_id="change",
    evidence=(Evidence("e1", "La métrica supera el umbral", "DW", 0.9),),
)

result = compile_decision(case)
print(result.verdict, result.readiness_score)
```

Prueba completa: `python src/thinking_patterns/examples/decision_compiler_demo.py`.


## 🚦 Decision Quality SDK v0.3

La capa de Decision Intelligence también puede ejecutarse fuera de Python como un **quality gate de CI**.

```bash
pip install -e .
decision-compile examples/decisions/pricing_raise.json --require-ready
```

El comando:

- lee un `DecisionCase` JSON versionable;
- ejecuta la revisión adversarial determinística;
- imprime `readiness_score`, dimensiones y findings como JSON;
- devuelve exit code `2` cuando `--require-ready` y la decisión no está lista;
- puede bloquear un deploy, promoción de modelo o cambio de política antes de producción.

Contrato portable: `schema/decision-case.schema.json`.

### Ejemplo en GitHub Actions

```yaml
- name: Gate decision quality
  run: decision-compile decisions/pricing.json --require-ready --compact
```

Esto permite que una decisión comercial o analítica tenga el mismo tratamiento que código: **versionada, testeable, revisable y con condiciones explícitas para actuar**.
