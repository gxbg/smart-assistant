from pydantic import BaseModel, Field
from typing import Optional


class ClassificacaoSchema(BaseModel):
    tipo: str = Field(description="reclamacao|duvida|elogio|sugestao")
    urgencia: str = Field(description="alta|media|baixa")
    tema: str = Field(description="Tema principal da mensagem")
    resumo: str = Field(description="Resumo curto da mensagem do cliente")


class ProcessamentoSchema(BaseModel):
    tipo_detectado: str = Field(description="Tipo que veio da etapa 1")
    dados_extraidos: dict = Field(description="Dados relevantes extraidos da mensagem")
    analise: str = Field(description="Analise detalhada da situacao")
    sentimento: Optional[str] = Field(default=None, description="positivo|negativo|neutro")
    prioridade: Optional[str] = Field(default=None, description="alta|media|baixa")


class RespostaSchema(BaseModel):
    resposta: str = Field(description="Resposta completa para o cliente")
    confianca: str = Field(description="alta|media|baixa")
    acao_sugerida: str = Field(description="Proxima acao recomendada")
    tempo_resolucao: Optional[str] = Field(default=None, description="Estimativa de tempo")
