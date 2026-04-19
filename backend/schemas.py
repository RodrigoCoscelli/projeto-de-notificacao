from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class UsuarioBase(BaseModel):
    username: str
    setor: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True

class NotificacaoBase(BaseModel):
    data_ocorrencia: date
    descricao_evento: str
    setor_sugerido: str

class NotificacaoCreateAnonima(NotificacaoBase):
    # Apenas os campos base + anonimato tratado no endpoint
    pass

class NotificacaoTriagem(BaseModel):
    setor_notificado_definitivo: str
    tipo_evento: str
    risco_frequencia: int
    risco_impacto: int
    # O NSP pode encerrar diretamente passando status Encerrada
    status: Optional[str] = "Pendente no Setor"

class NotificacaoResposta(BaseModel):
    justificativa_analise: str
    tratativa_acao: str

class NotificacaoPublic(BaseModel):
    protocolo_acompanhamento: str
    status: str
    tratativa_acao: Optional[str] = None
    data_criacao: datetime

class Notificacao(NotificacaoBase):
    id: int
    protocolo_acompanhamento: str
    usuario_notificador: Optional[str] = None
    setor_notificador: Optional[str] = None
    caminho_arquivo_evidencia: Optional[str] = None
    setor_notificado_definitivo: Optional[str] = None
    tipo_evento: Optional[str] = None
    status: str
    risco_frequencia: Optional[int] = None
    risco_impacto: Optional[int] = None
    nivel_risco_calculado: Optional[str] = None
    justificativa_analise: Optional[str] = None
    tratativa_acao: Optional[str] = None
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
