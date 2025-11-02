from __future__ import annotations
from typing import Dict, Any
from .idea_pattern import IdeaPattern

class LoggingComoNarrativa(IdeaPattern):
    def __init__(self) -> None:
        super().__init__(
            nombre="Logging→Narrativa",
            intencion="Hacer visible y trazable el razonamiento",
            analogia="logging estructurado",
            regla="Cuando haces logging, narras tu proceso.",
            transferencia="Metacognición y trazabilidad",
            hook="Añade 'Por qué' y 'Evidencia' a cada log",
            ejemplo="ETL: loggeo antes/después con tamaño y validaciones",
            antipatron="Logs verbosos sin decisión",
            metrica="% de commits con rationale en el mensaje",
        )

    def aplicar(self, contexto: Dict[str, Any]) -> str:
        paso = contexto.get("paso", "desconocido")
        decision = contexto.get("decision", "N/A")
        evidencia = contexto.get("evidencia", "sin evidencia")
        return f"[{paso}] Decisión: {decision} (evidencia: {evidencia}). → {self.regla}"

class DocstringComoHipotesis(IdeaPattern):
    def __init__(self) -> None:
        super().__init__(
            nombre="Docstring→Hipótesis",
            intencion="Explicar supuestos y límites de una función",
            analogia="docstrings y contratos",
            regla="Cuando documentas funciones, aprendes a explicar hipótesis.",
            transferencia="Claridad explicativa y diseño por contrato",
            hook="Secciones: Supuestos | Limitaciones | Ejemplos",
            ejemplo="Función con doctrinas GIVEN/WHEN/THEN",
            antipatron="Comentarios redundantes que no prueban nada",
            metrica="% de funciones con docstrings de 3 secciones",
        )

    def aplicar(self, contexto: Dict[str, Any]) -> str:
        funcion = contexto.get("funcion", "función_sin_nombre")
        supuesto = contexto.get("supuesto", "—")
        return f"{funcion} :: Supuesto clave: {supuesto}. → {self.regla}"

class ModularizacionComoPensamiento(IdeaPattern):
    def __init__(self) -> None:
        super().__init__(
            nombre="Modularización→Pensamiento",
            intencion="Separar preocupaciones para pensar mejor",
            analogia="separación de capas y módulos",
            regla="Cuando modularizas código, modularizas pensamientos.",
            transferencia="Enfoque y composición de ideas",
            hook="Divide en: preguntas, supuestos, decisiones",
            ejemplo="Pipeline separado en preproc/modelo/evaluación",
            antipatron="Módulos anémicos sin responsabilidad clara",
            metrica="Nº de dependencias cruzadas por módulo",
        )

    def aplicar(self, contexto: Dict[str, Any]) -> str:
        dominio = contexto.get("dominio", "proyecto")
        return f"{dominio}: separar preguntas, supuestos y decisiones. → {self.regla}"
