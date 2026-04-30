import os
import smtplib
from email.message import EmailMessage
from typing import List
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

def enviar_email(destinatarios: List[str], assunto: str, corpo: str):
    if not destinatarios:
        return
    
    # Remover e-mails vazios ou nulos
    destinatarios_validos = [d for d in destinatarios if d]
    if not destinatarios_validos:
        return

    # Se as credenciais não estiverem configuradas, apenas loga no console
    if not SMTP_USER or not SMTP_PASSWORD:
        print("\n" + "="*50)
        print("SIMULAÇÃO DE ENVIO DE E-MAIL (Credenciais não configuradas)")
        print(f"Para: {', '.join(destinatarios_validos)}")
        print(f"Assunto: {assunto}")
        print("-" * 50)
        print(corpo)
        print("="*50 + "\n")
        return

    try:
        msg = EmailMessage()
        msg.set_content(corpo)
        msg['Subject'] = assunto
        msg['From'] = SMTP_USER
        msg['To'] = ", ".join(destinatarios_validos)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            
        print(f"E-mail enviado com sucesso para: {destinatarios_validos}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
