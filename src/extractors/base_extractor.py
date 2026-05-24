from abc import ABC, abstractmethod
from src.validators.financial_validator import FinancialAnalysisResponse


class BaseExtractor(ABC):
    """
    Contrato abstrato para qualquer extrator de análise financeira.

    Princípio Open/Closed: o sistema está aberto para extensão (criar
    OpenAIExtractor, ClaudeExtractor, etc.) sem precisar modificar
    o código existente que depende desta interface.
    """

    @abstractmethod
    def analyze_expenses(self, transactions: list) -> FinancialAnalysisResponse:
        pass
