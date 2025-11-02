from __future__ import annotations
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
from typing import Dict, Any

@dataclass
class IdeaPattern(ABC):
    """Superclase para patrones de pensamiento inspirados en prácticas de ingeniería."""
    nombre: str
    intencion: str
    analogia: str
    regla: str
    transferencia: str
    hook: str
    ejemplo: str
    antipatron: str
    metrica: str

    @abstractmethod
    def aplicar(self, contexto: Dict[str, Any]) -> str:
        """Aplica el patrón a un contexto y devuelve una línea/aforismo contextualizado."""
        ...

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)
