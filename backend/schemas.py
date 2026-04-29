from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class ConfiguracaoPrazo(BaseModel):
    classificacao_risco: str
    prazo_dias: int
    prazo_horas: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True

class ConfiguracaoPrazosUpdate(BaseModel):
    prazos: List[ConfiguracaoPrazo]

class PlanoAcaoBase(BaseModel):
    o_que: str
    por_que: str
    onde: str
    quando: str
    quem: str
    como: str
    quanto_custa: str

class PlanoAcao(PlanoAcaoBase):
    id: int
    status: str
    data_criacao: datetime
    data_aprovacao: Optional[datetime] = None
    data_conclusao: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True

class UsuarioBase(BaseModel):
    username: str
    email: Optional[str] = None
    setor: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True

class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UsuarioAdminUpdate(BaseModel):
    setor: Optional[str] = None


class NotificacaoBase(BaseModel):
    data_ocorrencia: date
    descricao_evento: str
    setor_sugerido: str
    # Campos opcionais de produto
    produto_descricao: Optional[str] = None
    produto_codigo: Optional[str] = None
    produto_fabricante: Optional[str] = None
    produto_registro_ms: Optional[str] = None
    produto_lote_serie: Optional[str] = None
    produto_validade: Optional[str] = None

class NotificacaoCreateAnonima(NotificacaoBase):
    # Apenas os campos base + anonimato tratado no endpoint
    pass

class NotificacaoTriagem(BaseModel):
    setor_notificado_definitivo: Optional[str] = None
    tipo_evento: Optional[str] = None
    classificacao_risco: Optional[str] = None
    classificacao_meta_internacional: Optional[str] = None
    motivo_encerramento: Optional[str] = None
    # O NSP pode encerrar diretamente passando status Encerrada
    status: Optional[str] = "Pendente no Setor"
    requer_plano_acao: Optional[bool] = False

class NotificacaoResposta(BaseModel):
    justificativa_analise: str
    tratativa_acao: str
    plano_acao: Optional[PlanoAcaoBase] = None

class NotificacaoPublic(BaseModel):
    protocolo_acompanhamento: str
    status: str
    justificativa_analise: Optional[str] = None
    tratativa_acao: Optional[str] = None
    data_criacao: datetime
    plano_acao: Optional[PlanoAcao] = None

class Notificacao(NotificacaoBase):
    id: int
    protocolo_acompanhamento: str
    usuario_notificador: Optional[str] = None
    setor_notificador: Optional[str] = None
    caminho_arquivo_evidencia: Optional[str] = None
    setor_notificado_definitivo: Optional[str] = None
    tipo_evento: Optional[str] = None
    classificacao_risco: Optional[str] = None
    classificacao_meta_internacional: Optional[str] = None
    status: str
    justificativa_analise: Optional[str] = None
    tratativa_acao: Optional[str] = None
    motivo_encerramento: Optional[str] = None
    produto_descricao: Optional[str] = None
    produto_codigo: Optional[str] = None
    produto_fabricante: Optional[str] = None
    produto_registro_ms: Optional[str] = None
    produto_lote_serie: Optional[str] = None
    produto_validade: Optional[str] = None
    data_criacao: datetime
    data_triagem_nsp: Optional[datetime] = None
    data_resposta_setor: Optional[datetime] = None
    data_prazo_limite: Optional[datetime] = None
    bloqueado_por_atraso: bool = False
    requer_plano_acao: bool
    plano_acao: Optional[PlanoAcao] = None

    class Config:
        orm_mode = True
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
