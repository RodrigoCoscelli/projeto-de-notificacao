from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import models, database
from .routers import auth, notificacoes, reports, users

app = FastAPI(title="Notifica AME PG API")

# Criar tabelas se não existirem (forma simples sem alembic estrito para esta POC)
models.Base.metadata.create_all(bind=database.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir Rotas
app.include_router(auth.router)
app.include_router(notificacoes.router)
app.include_router(reports.router)
app.include_router(users.router)

# Montar arquivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
