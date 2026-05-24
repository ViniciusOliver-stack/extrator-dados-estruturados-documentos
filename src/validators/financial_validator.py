from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import date

class TransactionInsight(BaseModel):
    transaction_date: date = Field(description="Data da transação obtida do OFX")
    amount: float = Field(description="Valor da transação")
    original_description: str = Field(description="Descrição original que estava no OFX")
    
    # Requisitos:
    category: str = Field(description="Categoria do gasto (ex: Alimentação, Transporte, Lazer, Assinaturas)")
    is_recurring: bool = Field(description="Identifica se este padrão de gasto parece ser recorrente (ex: Uber frequente, cursos, assinaturas)")
    is_superfluous: bool = Field(description="True se o gasto puder ser evitado ou reduzido sem impactar as necessidades básicas")
    justification: str = Field(description="Justificativa clara do porquê esse gasto foi classificado como supérfluo ou essencial")
    priority: int = Field(description="Nível de prioridade de 1 (Alta/Essencial) a 3 (Baixa/Supérfluo)")
    saving_tip: str = Field(description="Dica prática e direta de como o cliente pode economizar ou otimizar esse ponto específico")
    
    @field_validator('priority')
    @classmethod
    def validate_priority_range(cls, value: int) -> int:
        if value < 1 or value > 3:
            raise ValueError("O nível de prioridade deve ser estritamente entre 1 e 3.")
        return value
    
class FinancialAnalysisResponse(BaseModel):
    transactions: List[TransactionInsight]
    global_insights: str = Field(description="Resumo macro da saúde financeira do período analisado e principais pontos de atenção")
