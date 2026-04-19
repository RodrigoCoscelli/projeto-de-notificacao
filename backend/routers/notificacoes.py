from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
import uuid

from .. import models, schemas, database
from .auth import get_current_user

router = APIRouter(prefix="/api/notificacoes", tags=["notificacoes"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def gerar_protocolo():
    import random
    import string
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"AMB-{random_str}"

def calcular_nivel_risco(freq: int, impacto: int) -> str:
    # Matriz 5x5 simples: multiplicando os valores
    score = freq * impacto
    if score <= 4:
        return "Baixo"
    elif score <= 9:
        return "Médio"
    elif score <= 16:
        return "Alto"
    else:
        return "Crítico"

from datetime import datetime

@router.post("", response_model=schemas.NotificacaoPublic)
def criar_notificacao(
    data_ocorrencia: str = Form(...),
    descricao_evento: str = Form(...),
    setor_sugerido: str = Form(...),
    anonimo: bool = Form(False),
    arquivo: Optional[UploadFile] = File(None),
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    # Tratar upload se existir
    file_path = None
    if arquivo:
        filename = f"{uuid.uuid4()}_{arquivo.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(arquivo.file, buffer)

    protocolo = gerar_protocolo()
    
    # Determinar autor: anônimo ou usuário logado
    setor_notif = current_user.setor
    if anonimo:
        usuario_notif = "Anônimo"
    else:
        usuario_notif = current_user.username
    
    # Converter string (YYYY-MM-DD) para date
    dt_ocorrencia = datetime.strptime(data_ocorrencia, "%Y-%m-%d").date()
    
    db_notificacao = models.Notificacao(
        protocolo_acompanhamento=protocolo,
        usuario_notificador=usuario_notif,
        setor_notificador=setor_notif,
        data_ocorrencia=dt_ocorrencia,
        descricao_evento=descricao_evento,
        setor_sugerido=setor_sugerido,
        caminho_arquivo_evidencia=file_path,
        status="Aguardando Triagem NSP"
    )
    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)
    return db_notificacao

@router.get("/public/{protocolo}", response_model=schemas.NotificacaoPublic)
def get_publica(protocolo: str, db: Session = Depends(database.get_db)):
    notificacao = db.query(models.Notificacao).filter(models.Notificacao.protocolo_acompanhamento == protocolo).first()
    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    return notificacao

@router.get("", response_model=List[schemas.Notificacao])
def listar_notificacoes(db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    if current_user.setor == "NSP":
        return db.query(models.Notificacao).all()
    else:
        from sqlalchemy import or_, and_
        # Mostra as que ele recebeu OU as que ele criou
        return db.query(models.Notificacao).filter(
            or_(
                and_(
                    models.Notificacao.setor_notificado_definitivo == current_user.setor,
                    models.Notificacao.status.in_(["Pendente no Setor", "Respondida"])
                ),
                models.Notificacao.setor_notificador == current_user.setor
            )
        ).all()

@router.get("/{id}", response_model=schemas.Notificacao)
def obter_notificacao(id: int, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    notificacao = db.query(models.Notificacao).filter(models.Notificacao.id == id).first()
    if not notificacao:
        raise HTTPException(status_code=404, detail="Não encontrada")
    return notificacao

@router.put("/{id}/triagem", response_model=schemas.Notificacao)
def triagem_nsp(id: int, triagem: schemas.NotificacaoTriagem, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    if current_user.setor != "NSP":
        raise HTTPException(status_code=403, detail="Apenas NSP pode realizar triagem")
    
    notificacao = db.query(models.Notificacao).filter(models.Notificacao.id == id).first()
    if not notificacao:
        raise HTTPException(status_code=404, detail="Não encontrada")

    notificacao.tipo_evento = triagem.tipo_evento
    notificacao.setor_notificado_definitivo = triagem.setor_notificado_definitivo
    notificacao.risco_frequencia = triagem.risco_frequencia
    notificacao.risco_impacto = triagem.risco_impacto
    notificacao.nivel_risco_calculado = calcular_nivel_risco(triagem.risco_frequencia, triagem.risco_impacto)
    notificacao.data_triagem_nsp = datetime.now()
    
    # Pode ser que o NSP já decida encerrar (ex: "Não cabe notificação")
    notificacao.status = triagem.status
    
    db.commit()
    db.refresh(notificacao)
    return notificacao

@router.put("/{id}/resposta", response_model=schemas.Notificacao)
def resposta_setor(id: int, resposta: schemas.NotificacaoResposta, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    notificacao = db.query(models.Notificacao).filter(models.Notificacao.id == id).first()
    if not notificacao:
        raise HTTPException(status_code=404, detail="Não encontrada")

    if notificacao.setor_notificado_definitivo != current_user.setor:
        raise HTTPException(status_code=403, detail="Você não pertence ao setor notificado desta ocorrência")

    notificacao.justificativa_analise = resposta.justificativa_analise
    notificacao.tratativa_acao = resposta.tratativa_acao
    notificacao.data_resposta_setor = datetime.now()
    notificacao.status = "Respondida" # Fluxo encerra como Respondida nesta POC, conforme solicitado
    
    db.commit()
    db.refresh(notificacao)
    return notificacao
