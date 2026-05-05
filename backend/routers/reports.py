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

def format_datetime(dt):
    """Formata datetime para string ou retorna None"""
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def format_date(dt):
    """Formata date para string ou retorna None"""
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%d")

@router.get("/powerbi")
def get_relatorio_powerbi(api_key: str = Depends(verify_api_key), db: Session = Depends(database.get_db)):
    notificacoes = db.query(models.Notificacao).all()
    resultado = []
    
    for n in notificacoes:
        # Calcular dias em aberto
        dias_aberto = 0
        if n.status in ["Aguardando Triagem NSP", "Pendente no Setor"]:
            dias_aberto = (datetime.now().date() - n.data_criacao.date()).days
        elif n.data_resposta_setor:
            dias_aberto = (n.data_resposta_setor.date() - n.data_criacao.date()).days
        elif n.data_triagem_nsp:
            dias_aberto = (n.data_triagem_nsp.date() - n.data_criacao.date()).days

        pa = n.plano_acao
        
        resultado.append({
            "ID": n.id,
            "Protocolo": n.protocolo_acompanhamento,
            "Usuario Notificador": n.usuario_notificador,
            "Setor Notificador": n.setor_notificador,
            "Data Ocorrencia": format_date(n.data_ocorrencia),
            "Descricao Evento": n.descricao_evento,
            "Setor Sugerido": n.setor_sugerido,
            "Setor Definitivo": n.setor_notificado_definitivo,
            "Tipo Evento": n.tipo_evento,
            "Classificacao Risco": n.classificacao_risco,
            "Meta Internacional": n.classificacao_meta_internacional,
            "Status": n.status,
            "Justificativa Analise": n.justificativa_analise,
            "Tratativa Acao": n.tratativa_acao,
            "Motivo Encerramento": n.motivo_encerramento,
            "Data Criacao": format_datetime(n.data_criacao),
            "Data Triagem NSP": format_datetime(n.data_triagem_nsp),
            "Data Resposta Setor": format_datetime(n.data_resposta_setor),
            "Data Prazo Limite": format_datetime(n.data_prazo_limite),
            "Atrasada": "Sim" if n.bloqueado_por_atraso else "Nao",
            "Dias Aberto": max(0, dias_aberto),
            "Requer Plano Acao": "Sim" if n.requer_plano_acao else "Nao",
            "Produto Descricao": n.produto_descricao,
            "Produto Codigo": n.produto_codigo,
            "Produto Fabricante": n.produto_fabricante,
            "Produto Registro MS": n.produto_registro_ms,
            "Produto Lote Serie": n.produto_lote_serie,
            "Produto Validade": n.produto_validade,
            "Plano Acao Status": pa.status if pa else None,
            "Plano O que": pa.o_que if pa else None,
            "Plano Por que": pa.por_que if pa else None,
            "Plano Onde": pa.onde if pa else None,
            "Plano Quando": pa.quando if pa else None,
            "Plano Quem": pa.quem if pa else None,
            "Plano Como": pa.como if pa else None,
            "Plano Quanto Custa": pa.quanto_custa if pa else None,
            "Plano Data Aprovacao": format_datetime(pa.data_aprovacao) if pa else None,
            "Plano Data Conclusao": format_datetime(pa.data_conclusao) if pa else None
        })
    
    return resultado
