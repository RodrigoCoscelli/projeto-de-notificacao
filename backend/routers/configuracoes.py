from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database
from .auth import get_current_user

router = APIRouter(prefix="/api/configuracoes", tags=["configuracoes"])

CLASSIFICACOES_PADRAO = [
    {"classificacao_risco": "Near miss", "prazo_dias": 7, "prazo_horas": None},
    {"classificacao_risco": "Incidente sem dano", "prazo_dias": 7, "prazo_horas": None},
    {"classificacao_risco": "Evento Adverso leve", "prazo_dias": 5, "prazo_horas": None},
    {"classificacao_risco": "Evento Adverso moderado", "prazo_dias": 3, "prazo_horas": None},
    {"classificacao_risco": "Evento Adverso grave", "prazo_dias": 2, "prazo_horas": None},
    {"classificacao_risco": "Óbito/Never Events", "prazo_dias": 0, "prazo_horas": 5},
    {"classificacao_risco": "Outros", "prazo_dias": 7, "prazo_horas": None},
]

@router.get("/prazos", response_model=List[schemas.ConfiguracaoPrazo])
def listar_prazos(db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    prazos = db.query(models.ConfiguracaoPrazo).all()
    
    # Se ainda não há prazos configurados, retornar os padrões
    if not prazos:
        return [schemas.ConfiguracaoPrazo(**p) for p in CLASSIFICACOES_PADRAO]
    
    return prazos

@router.put("/prazos", response_model=List[schemas.ConfiguracaoPrazo])
def salvar_prazos(payload: schemas.ConfiguracaoPrazosUpdate, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    if current_user.setor != "NSP":
        raise HTTPException(status_code=403, detail="Apenas NSP pode configurar prazos")
    
    for item in payload.prazos:
        existente = db.query(models.ConfiguracaoPrazo).filter(
            models.ConfiguracaoPrazo.classificacao_risco == item.classificacao_risco
        ).first()
        
        if existente:
            existente.prazo_dias = item.prazo_dias
            existente.prazo_horas = item.prazo_horas
        else:
            novo = models.ConfiguracaoPrazo(
                classificacao_risco=item.classificacao_risco,
                prazo_dias=item.prazo_dias,
                prazo_horas=item.prazo_horas
            )
            db.add(novo)
    
    db.commit()
    return db.query(models.ConfiguracaoPrazo).all()

@router.get("/setores", response_model=List[schemas.Setor])
def listar_setores(db: Session = Depends(database.get_db)):
    setores = db.query(models.Setor).order_by(models.Setor.nome).all()
    if not setores:
        setores_padrao = [
            "NSP", "Recepção", "Enfermagem", "Farmácia", "Centro Cirúrgico",
            "Serviços Gerais", "Equipe médica", "Controladoria", "Financeiro", "Compras", "Qualidade"
        ]
        for s in setores_padrao:
            db.add(models.Setor(nome=s))
        db.commit()
        setores = db.query(models.Setor).order_by(models.Setor.nome).all()
    return setores

@router.post("/setores", response_model=schemas.Setor)
def criar_setor(setor: schemas.SetorCreate, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    if current_user.setor != "NSP":
        raise HTTPException(status_code=403, detail="Apenas NSP pode gerenciar setores")
    
    existente = db.query(models.Setor).filter(models.Setor.nome == setor.nome).first()
    if existente:
        raise HTTPException(status_code=400, detail="Setor já existe")
        
    novo = models.Setor(nome=setor.nome)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.delete("/setores/{setor_id}")
def deletar_setor(setor_id: int, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    if current_user.setor != "NSP":
        raise HTTPException(status_code=403, detail="Apenas NSP pode gerenciar setores")
        
    setor = db.query(models.Setor).filter(models.Setor.id == setor_id).first()
    if not setor:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
        
    if setor.nome == "NSP":
        raise HTTPException(status_code=400, detail="Não é possível excluir o setor NSP")
        
    db.delete(setor)
    db.commit()
    return {"detail": "Setor excluído com sucesso"}
