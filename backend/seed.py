from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, auth

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
    print("Banco repovoado com sucesso.")
    print("Usuários inseridos no banco: admin_nsp (NSP), farmacia (Farmácia), recepcao (Recepção), enfermagem (Enfermagem). Senha: senha123")
    
    db.close()

if __name__ == "__main__":
    seed_db()
