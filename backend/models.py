from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    setor = Column(String, nullable=False)

class Notificacao(Base):
    __tablename__ = "notificacoes"
    id = Column(Integer, primary_key=True, index=True)
    protocolo_acompanhamento = Column(String, unique=True, index=True, nullable=False)
    usuario_notificador = Column(String, nullable=True) # Pode ser 'Anônimo'
    setor_notificador = Column(String, nullable=True) # Pode ser 'Anônimo'
    data_ocorrencia = Column(Date, nullable=False)
    descricao_evento = Column(Text, nullable=False)
    caminho_arquivo_evidencia = Column(String, nullable=True)
    setor_sugerido = Column(String, nullable=False)
    setor_notificado_definitivo = Column(String, nullable=True)
    tipo_evento = Column(String, nullable=True)
    status = Column(String, nullable=False, default="Aguardando Triagem NSP")
    risco_frequencia = Column(Integer, nullable=True)
    risco_impacto = Column(Integer, nullable=True)
    nivel_risco_calculado = Column(String, nullable=True)
    justificativa_analise = Column(Text, nullable=True)
    tratativa_acao = Column(Text, nullable=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
