from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import models, database

router = APIRouter(prefix="/api/relatorios", tags=["relatorios"])

API_KEY_POWERBI = "ame-pg-powerbi-key"

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY_POWERBI:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@router.get("/powerbi")
def get_relatorio_powerbi(api_key: str = Depends(verify_api_key), db: Session = Depends(database.get_db)):
    notificacoes = db.query(models.Notificacao).all()
    resultado = []
    
    for n in notificacoes:
        # Calcular dias em aberto (se não encerrada/respondida, conta da criacao até hoje, senão conta ate atualizacao)
        dias_aberto = 0
        if n.status in ["Aguardando Triagem NSP", "Pendente no Setor"]:
            dias_aberto = (datetime.now().date() - n.data_criacao.date()).days
        elif n.data_atualizacao:
            dias_aberto = (n.data_atualizacao.date() - n.data_criacao.date()).days

        resultado.append({
            "Protocolo": n.protocolo_acompanhamento,
            "Setor Notificador": n.setor_notificador,
            "Data Ocorrencia": n.data_ocorrencia.strftime("%Y-%m-%d"),
            "Setor Definitivo": n.setor_notificado_definitivo or n.setor_sugerido,
            "Tipo Evento": n.tipo_evento or "Não classificado",
            "Nivel Risco": n.nivel_risco_calculado or "N/A",
            "Status": n.status,
            "Dias Aberto": max(0, dias_aberto),
            "Data Criacao": n.data_criacao.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return resultado
