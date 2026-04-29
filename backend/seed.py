from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, auth
from datetime import timedelta

def seed_db():
    print("Limpando banco de dados...")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()

    nsp_user = models.Usuario(
        username="admin_nsp",
        password_hash=auth.get_password_hash("senha123"),
        setor="NSP"
    )
    farmacia_user = models.Usuario(
        username="farmacia",
        password_hash=auth.get_password_hash("senha123"),
        setor="Farmácia"
    )
    recepcao_user = models.Usuario(
        username="recepcao",
        password_hash=auth.get_password_hash("senha123"),
        setor="Recepção"
    )
    enfermagem_user = models.Usuario(
        username="enfermagem",
        password_hash=auth.get_password_hash("senha123"),
        setor="Enfermagem"
    )
    
    db.add_all([nsp_user, farmacia_user, recepcao_user, enfermagem_user])
    db.commit()

    # Inserir prazos padrão por classificação de risco
    prazos_padrao = [
        models.ConfiguracaoPrazo(classificacao_risco="Near miss", prazo_dias=7, prazo_horas=None),
        models.ConfiguracaoPrazo(classificacao_risco="Incidente sem dano", prazo_dias=7, prazo_horas=None),
        models.ConfiguracaoPrazo(classificacao_risco="Evento Adverso leve", prazo_dias=5, prazo_horas=None),
        models.ConfiguracaoPrazo(classificacao_risco="Evento Adverso moderado", prazo_dias=3, prazo_horas=None),
        models.ConfiguracaoPrazo(classificacao_risco="Evento Adverso grave", prazo_dias=2, prazo_horas=None),
        models.ConfiguracaoPrazo(classificacao_risco="Óbito/Never Events", prazo_dias=0, prazo_horas=5),
        models.ConfiguracaoPrazo(classificacao_risco="Outros", prazo_dias=7, prazo_horas=None),
    ]
    db.add_all(prazos_padrao)
    db.commit()

    print("Banco repovoado com sucesso.")
    print("Usuários inseridos no banco: admin_nsp (NSP), farmacia (Farmácia), recepcao (Recepção), enfermagem (Enfermagem). Senha: senha123")
    
    db.close()

if __name__ == "__main__":
    seed_db()
