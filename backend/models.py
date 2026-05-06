from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Setor(Base):
    __tablename__ = "setores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)

class ConfiguracaoPrazo(Base):
    __tablename__ = "configuracoes_prazo"
    id = Column(Integer, primary_key=True, index=True)
    classificacao_risco = Column(String, unique=True, nullable=False, index=True)
    prazo_dias = Column(Integer, nullable=False)  # -1 = horas (apenas para Óbito), positivo = dias
    prazo_horas = Column(Integer, nullable=True)  # usado quando prazo é em horas (ex: Óbito = 5)

class PlanoAcao(Base):
    __tablename__ = "planos_acao"
    id = Column(Integer, primary_key=True, index=True)
    o_que = Column(Text, nullable=False)
    por_que = Column(Text, nullable=False)
    onde = Column(Text, nullable=False)
    quando = Column(Text, nullable=False)
    quem = Column(Text, nullable=False)
    como = Column(Text, nullable=False)
    quanto_custa = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="Aguardando Análise NSP")
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_aprovacao = Column(DateTime(timezone=True), nullable=True)
    data_conclusao = Column(DateTime(timezone=True), nullable=True)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=True)
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
    classificacao_risco = Column(String, nullable=True)
    classificacao_meta_internacional = Column(String, nullable=True)
    justificativa_analise = Column(Text, nullable=True)
    tratativa_acao = Column(Text, nullable=True)
    motivo_encerramento = Column(Text, nullable=True)
    
    # Campos para Material/Medicamento/Equipamento

    produto_descricao = Column(String, nullable=True)
    produto_codigo = Column(String, nullable=True)
    produto_fabricante = Column(String, nullable=True)
    produto_registro_ms = Column(String, nullable=True)
    produto_lote_serie = Column(String, nullable=True)
    produto_validade = Column(String, nullable=True)
    
    requer_plano_acao = Column(Boolean, nullable=False, default=False)
    id_plano_acao = Column(Integer, ForeignKey("planos_acao.id"), nullable=True)
    
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_triagem_nsp = Column(DateTime(timezone=True), nullable=True)
    data_resposta_setor = Column(DateTime(timezone=True), nullable=True)
    data_prazo_limite = Column(DateTime(timezone=True), nullable=True)
    bloqueado_por_atraso = Column(Boolean, nullable=False, default=False)

    plano_acao = relationship("PlanoAcao")

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    token = Column(String, nullable=False, index=True)  # código de 6 dígitos
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
