from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
import uuid

from .. import models, schemas, database
from .auth import get_current_user
from ..email_service import enviar_email

router = APIRouter(prefix="/api/notificacoes", tags=["notificacoes"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def gerar_protocolo(db: Session):
    import random
    import string
    while True:
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        protocolo = f"AMB-{random_str}"
        # Verificar se já existe no banco
        existe = db.query(models.Notificacao).filter(models.Notificacao.protocolo_acompanhamento == protocolo).first()
        if not existe:
            return protocolo


from datetime import datetime, timedelta

@router.post("", response_model=schemas.NotificacaoPublic)
def criar_notificacao(
    background_tasks: BackgroundTasks,
    data_ocorrencia: str = Form(...),
    descricao_evento: str = Form(...),
    setor_sugerido: str = Form(...),
    anonimo: bool = Form(False),
    arquivo: Optional[UploadFile] = File(None),
    produto_descricao: Optional[str] = Form(None),
    produto_codigo: Optional[str] = Form(None),
    produto_fabricante: Optional[str] = Form(None),
    produto_registro_ms: Optional[str] = Form(None),
    produto_lote_serie: Optional[str] = Form(None),
    produto_validade: Optional[str] = Form(None),
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    # Tratar upload se existir
    file_path = None
    if arquivo:
        filename = f"{arquivo.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(arquivo.file, buffer)

    protocolo = gerar_protocolo(db)
    
    # Determinar autor: anônimo ou usuário logado
    if anonimo:
        usuario_notif = "Anônimo"
        setor_notif = "Anônimo"
    else:
        usuario_notif = current_user.username
        setor_notif = current_user.setor
    
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
        status="Aguardando Triagem NSP",
        produto_descricao=produto_descricao,
        produto_codigo=produto_codigo,
        produto_fabricante=produto_fabricante,
        produto_registro_ms=produto_registro_ms,
        produto_lote_serie=produto_lote_serie,
        produto_validade=produto_validade
    )
    db.add(db_notificacao)
    db.commit()
    db.refresh(db_notificacao)
    
    # Enviar e-mail para a NSP
    usuarios_nsp = db.query(models.Usuario.email).filter(models.Usuario.setor == "NSP", models.Usuario.email.isnot(None)).all()
    emails_nsp = [u[0] for u in usuarios_nsp if u[0]]
    if emails_nsp:
        assunto = f"Nova Notificação Registrada - Protocolo {protocolo}"
        corpo = f"Uma nova notificação foi registrada no sistema.\nProtocolo: {protocolo}\nPor favor, acesse o sistema para realizar a triagem.\n\nAtenciosamente, Sistema Notifica AMEPG"
        background_tasks.add_task(enviar_email, emails_nsp, assunto, corpo)

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
                    models.Notificacao.status.in_(["Pendente no Setor", "Aguardando Plano de Ação 5W2H", "Plano de Ação Recusado", "Respondida", "Plano em Análise NSP", "Aguardando Conclusão do Plano", "Encerrada"])
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
def triagem_nsp(id: int, triagem: schemas.NotificacaoTriagem, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    if current_user.setor != "NSP":
        raise HTTPException(status_code=403, detail="Apenas NSP pode realizar triagem")
    
    notificacao = db.query(models.Notificacao).filter(models.Notificacao.id == id).first()
    if not notificacao:
        raise HTTPException(status_code=404, detail="Não encontrada")

    notificacao.tipo_evento = triagem.tipo_evento
    notificacao.setor_notificado_definitivo = triagem.setor_notificado_definitivo
    notificacao.classificacao_risco = triagem.classificacao_risco
    notificacao.classificacao_meta_internacional = triagem.classificacao_meta_internacional
    
    # Se o NSP encerrar diretamente, salva o motivo de encerramento
    if triagem.motivo_encerramento:
        notificacao.motivo_encerramento = triagem.motivo_encerramento
    
    notificacao.requer_plano_acao = triagem.requer_plano_acao
    if triagem.requer_plano_acao and triagem.status != "Encerrada":
        notificacao.status = "Aguardando Plano de Ação 5W2H"
    else:
        notificacao.status = triagem.status
        
    notificacao.data_triagem_nsp = datetime.now()
    
    # Calcular prazo limite com base na classificação de risco
    if notificacao.classificacao_risco and notificacao.status != "Encerrada":
        prazo_config = db.query(models.ConfiguracaoPrazo).filter(
            models.ConfiguracaoPrazo.classificacao_risco == notificacao.classificacao_risco
        ).first()
        if prazo_config:
            if prazo_config.prazo_dias == 0 and prazo_config.prazo_horas:
                # Prazo em horas (ex: Óbito = 5 horas)
                notificacao.data_prazo_limite = datetime.now() + timedelta(hours=prazo_config.prazo_horas)
            else:
                notificacao.data_prazo_limite = datetime.now() + timedelta(days=prazo_config.prazo_dias)
    
    db.commit()
    db.refresh(notificacao)
    
    # Enviar e-mail para o setor notificado
    if notificacao.setor_notificado_definitivo:
        usuarios_setor = db.query(models.Usuario.email).filter(
            models.Usuario.setor == notificacao.setor_notificado_definitivo, 
            models.Usuario.email.isnot(None)
        ).all()
        emails_setor = [u[0] for u in usuarios_setor if u[0]]
        
        if emails_setor:
            assunto = f"Nova Notificação para seu Setor - Protocolo {notificacao.protocolo_acompanhamento}"
            corpo = f"Uma notificação foi validada pela NSP e direcionada ao seu setor ({notificacao.setor_notificado_definitivo}).\nProtocolo: {notificacao.protocolo_acompanhamento}\nStatus atual: {notificacao.status}\n\nPor favor, acesse o sistema para analisar e responder.\n Atenciosamente, Sistema Notifica AMEPG"
            background_tasks.add_task(enviar_email, emails_setor, assunto, corpo)

    return notificacao

@router.put("/{id}/resposta", response_model=schemas.Notificacao)
def resposta_setor(id: int, resposta: schemas.NotificacaoResposta, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    notificacao = db.query(models.Notificacao).filter(models.Notificacao.id == id).first()
    if not notificacao:
        raise HTTPException(status_code=404, detail="Não encontrada")

    if notificacao.setor_notificado_definitivo != current_user.setor:
        raise HTTPException(status_code=403, detail="Você não pertence ao setor notificado desta ocorrência")

    # Verificar se o prazo expirou e bloquear automaticamente
    if notificacao.data_prazo_limite and datetime.now() > notificacao.data_prazo_limite:
        if not notificacao.bloqueado_por_atraso:
            notificacao.bloqueado_por_atraso = True
            db.commit()
            db.refresh(notificacao)
        raise HTTPException(status_code=403, detail="Esta notificação está bloqueada por atraso no prazo. Solicite liberação ao NSP.")

    if notificacao.bloqueado_por_atraso:
        raise HTTPException(status_code=403, detail="Esta notificação está bloqueada por atraso no prazo. Solicite liberação ao NSP.")

    notificacao.justificativa_analise = resposta.justificativa_analise
    notificacao.tratativa_acao = resposta.tratativa_acao
    notificacao.data_resposta_setor = datetime.now()

    if notificacao.requer_plano_acao and resposta.plano_acao:
        if notificacao.plano_acao:
            # Update existing
            notificacao.plano_acao.o_que = resposta.plano_acao.o_que
            notificacao.plano_acao.por_que = resposta.plano_acao.por_que
            notificacao.plano_acao.onde = resposta.plano_acao.onde
            notificacao.plano_acao.quando = resposta.plano_acao.quando
            notificacao.plano_acao.quem = resposta.plano_acao.quem
            notificacao.plano_acao.como = resposta.plano_acao.como
            notificacao.plano_acao.quanto_custa = resposta.plano_acao.quanto_custa
            notificacao.plano_acao.status = "Aguardando Análise NSP"
        else:
            # Create new
            novo_plano = models.PlanoAcao(
                o_que=resposta.plano_acao.o_que,
                por_que=resposta.plano_acao.por_que,
                onde=resposta.plano_acao.onde,
                quando=resposta.plano_acao.quando,
                quem=resposta.plano_acao.quem,
                como=resposta.plano_acao.como,
                quanto_custa=resposta.plano_acao.quanto_custa,
                status="Aguardando Análise NSP"
            )
            db.add(novo_plano)
            db.flush()
            notificacao.id_plano_acao = novo_plano.id
            
        notificacao.status = "Plano em Análise NSP"
    else:
        notificacao.status = "Respondida"
    
    db.commit()
    db.refresh(notificacao)
    
    # Enviar e-mail para a NSP e para o criador da notificação
    destinatarios = []
    
    # Emails NSP
    usuarios_nsp = db.query(models.Usuario.email).filter(models.Usuario.setor == "NSP", models.Usuario.email.isnot(None)).all()
    destinatarios.extend([u[0] for u in usuarios_nsp if u[0]])
    
    # Email do criador (se não for anônimo)
    if notificacao.usuario_notificador and notificacao.usuario_notificador != "Anônimo":
        usuario_criador = db.query(models.Usuario.email).filter(
            models.Usuario.username == notificacao.usuario_notificador, 
            models.Usuario.email.isnot(None)
        ).first()
        if usuario_criador and usuario_criador[0]:
            destinatarios.append(usuario_criador[0])
            
    destinatarios = list(set(destinatarios)) # Remove duplicatas
    
    if destinatarios:
        assunto = f"Notificação Respondida - Protocolo {notificacao.protocolo_acompanhamento}"
        corpo = f"O setor {notificacao.setor_notificado_definitivo} respondeu à notificação.\nProtocolo: {notificacao.protocolo_acompanhamento}\nStatus atual: {notificacao.status}\nPor favor, acesse o sistema para conferir a resposta.\n\nAtenciosamente, Sistema Notifica AMEPG"
        background_tasks.add_task(enviar_email, destinatarios, assunto, corpo)

    return notificacao

class PlanoAcaoAnaliseSchema(schemas.BaseModel):
    status: str # "Aprovado" ou "Recusado"

@router.put("/{id}/plano_acao/analise", response_model=schemas.Notificacao)
def analise_plano_acao(id: int, analise: PlanoAcaoAnaliseSchema, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    if current_user.setor != "NSP":
        raise HTTPException(status_code=403, detail="Apenas NSP pode analisar planos de ação")
    
    notificacao = db.query(models.Notificacao).filter(models.Notificacao.id == id).first()
    if not notificacao or not notificacao.plano_acao:
        raise HTTPException(status_code=404, detail="Plano de ação não encontrado")

    if analise.status == "Aprovado":
        notificacao.plano_acao.status = "Em Andamento"
        notificacao.plano_acao.data_aprovacao = datetime.now()
        notificacao.status = "Aguardando Conclusão do Plano"
    elif analise.status == "Recusado":
        notificacao.plano_acao.status = analise.status
        notificacao.status = "Plano de Ação Recusado"
    
    db.commit()
    db.refresh(notificacao)
    return notificacao

@router.put("/{id}/plano_acao/concluir", response_model=schemas.Notificacao)
def concluir_plano_acao(id: int, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    notificacao = db.query(models.Notificacao).filter(models.Notificacao.id == id).first()
    if not notificacao or not notificacao.plano_acao:
        raise HTTPException(status_code=404, detail="Plano de ação não encontrado")

    if notificacao.setor_notificado_definitivo != current_user.setor:
        raise HTTPException(status_code=403, detail="Você não pertence ao setor responsável por este plano")

    if notificacao.plano_acao.status != "Em Andamento":
        raise HTTPException(status_code=400, detail="Plano de ação não está em andamento")

    notificacao.plano_acao.status = "Concluído"
    notificacao.plano_acao.data_conclusao = datetime.now()
    notificacao.status = "Encerrada"
    
    db.commit()
    db.refresh(notificacao)
    return notificacao

class DesbloquearSchema(schemas.BaseModel):
    dias_extras: int  # Dias extras a serem adicionados ao prazo

@router.put("/{id}/desbloquear", response_model=schemas.Notificacao)
def desbloquear_notificacao(id: int, payload: DesbloquearSchema, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    if current_user.setor != "NSP":
        raise HTTPException(status_code=403, detail="Apenas NSP pode desbloquear notificações")
    
    notificacao = db.query(models.Notificacao).filter(models.Notificacao.id == id).first()
    if not notificacao:
        raise HTTPException(status_code=404, detail="Não encontrada")
    
    notificacao.bloqueado_por_atraso = False
    # Estender prazo a partir de agora
    notificacao.data_prazo_limite = datetime.now() + timedelta(days=payload.dias_extras)
    
    db.commit()
    db.refresh(notificacao)
    return notificacao
