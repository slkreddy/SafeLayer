from abc import ABC, abstractmethod
from typing import Any, Dict, List

class BaseGuard(ABC):
    def __init__(self, explain: bool = False):
        self.explain = explain

    @abstractmethod
    def check(self, text: str) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def mask(self, text: str) -> str:
        ...

    def explain_action(self, details: Dict[str, Any]):
        if self.explain:
            print(f"[{self.__class__.__name__}][EXPLAIN]", details.get("explanation", ""))
