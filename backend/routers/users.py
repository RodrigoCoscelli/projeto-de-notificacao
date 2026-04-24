from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database, auth
from .auth import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("", response_model=List[schemas.Usuario])
def list_users(current_user: models.Usuario = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if current_user.username != "admin_nsp":
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas o admin_nsp pode listar usuários.")
    return db.query(models.Usuario).all()

@router.post("", response_model=schemas.Usuario)
def create_user(user: schemas.UsuarioCreate, current_user: models.Usuario = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if current_user.username != "admin_nsp":
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas o admin_nsp pode criar usuários.")
    
    existing_user = db.query(models.Usuario).filter(models.Usuario.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username já cadastrado.")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.Usuario(username=user.username, email=user.email, password_hash=hashed_password, setor=user.setor)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: models.Usuario = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if current_user.username != "admin_nsp":
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas o admin_nsp pode excluir usuários.")
    
    user_to_delete = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        
    db.delete(user_to_delete)
    db.commit()
    return {"detail": "Usuário excluído com sucesso."}

@router.put("/me", response_model=schemas.Usuario)
def update_me(user_update: schemas.UsuarioUpdate, current_user: models.Usuario = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if user_update.username:
        existing_user = db.query(models.Usuario).filter(models.Usuario.username == user_update.username).first()
        if existing_user and existing_user.id != current_user.id:
             raise HTTPException(status_code=400, detail="Username já em uso por outro usuário.")
        current_user.username = user_update.username
        
    if user_update.email is not None:
        current_user.email = user_update.email
        
    if user_update.password:
        current_user.password_hash = auth.get_password_hash(user_update.password)
        
    db.commit()
    db.refresh(current_user)
    return current_user
