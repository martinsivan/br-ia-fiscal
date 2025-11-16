from abc import ABC, abstractmethod
from typing import List

class LLMClient(ABC):
    @abstractmethod
    def analyze_nfe(self, xml: str) -> List[str]:
        pass

# Vamos usar DeepSeek como padrão
from .deepseek import DeepSeekClient
client = DeepSeekClient()
