from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
import secrets

from .. import models, schemas, auth, database
from ..email_service import enviar_email

router = APIRouter(prefix="/api/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.Usuario).filter(models.Usuario.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    from sqlalchemy import or_
    user = db.query(models.Usuario).filter(
        or_(
            models.Usuario.username == form_data.username,
            models.Usuario.email == form_data.username,
        )
    ).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "setor": user.setor}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.Usuario)
def read_users_me(current_user: models.Usuario = Depends(get_current_user)):
    return current_user


# ─── Recuperação de Senha ───

@router.post("/forgot-password")
def forgot_password(
    request: schemas.ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db),
):
    """
    Gera um código de 6 dígitos e envia para o e-mail do usuário.
    Resposta genérica para não revelar se o usuário existe.
    """
    from sqlalchemy import or_
    user = db.query(models.Usuario).filter(
        or_(
            models.Usuario.username == request.username,
            models.Usuario.email == request.username,
        )
    ).first()

    if user and user.email:
        # Invalidar códigos anteriores do mesmo usuário
        db.query(models.PasswordResetToken).filter(
            models.PasswordResetToken.user_id == user.id,
            models.PasswordResetToken.used == False,
        ).update({"used": True})

        # Gerar código numérico de 6 dígitos
        code = f"{secrets.randbelow(1000000):06d}"

        # Salvar token com validade de 15 minutos
        reset_token = models.PasswordResetToken(
            user_id=user.id,
            token=code,
            expires_at=datetime.utcnow() + timedelta(minutes=15),
        )
        db.add(reset_token)
        db.commit()

        # Enviar e-mail em background
        assunto = "Notifica - Código de Recuperação de Senha"
        corpo = (
            f"Olá, {user.username}!\n\n"
            f"Você solicitou a recuperação de senha do sistema Notifica.\n\n"
            f"Seu código de verificação é:\n\n"
            f"    {code}\n\n"
            f"Este código expira em 15 minutos.\n\n"
            f"Se você não solicitou esta recuperação, ignore este e-mail.\n\n"
            f"— Equipe Notifica Ambulatório"
        )
        background_tasks.add_task(enviar_email, [user.email], assunto, corpo)

    # Sempre retorna sucesso (segurança contra enumeração de usuários)
    return {
        "message": "Se o usuário possuir um e-mail cadastrado, um código de recuperação foi enviado."
    }


@router.post("/reset-password")
def reset_password(
    request: schemas.ResetPasswordRequest,
    db: Session = Depends(database.get_db),
):
    """
    Valida o código de recuperação e define a nova senha.
    """
    from sqlalchemy import or_
    user = db.query(models.Usuario).filter(
        or_(
            models.Usuario.username == request.username,
            models.Usuario.email == request.username,
        )
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código inválido ou expirado.",
        )

    # Buscar token válido (não usado e não expirado)
    reset_token = db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.user_id == user.id,
        models.PasswordResetToken.token == request.code,
        models.PasswordResetToken.used == False,
        models.PasswordResetToken.expires_at > datetime.utcnow(),
    ).first()

    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código inválido ou expirado.",
        )

    if len(request.new_password) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A nova senha deve ter no mínimo 4 caracteres.",
        )

    # Atualizar senha
    user.password_hash = auth.get_password_hash(request.new_password)

    # Marcar token como usado
    reset_token.used = True

    db.commit()
    return {"message": "Senha alterada com sucesso."}
