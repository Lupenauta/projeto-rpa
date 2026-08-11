import os
import base64
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")


def conectar_gmail():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build(
        "gmail",
        "v1",
        credentials=creds
    )


def buscar_solicitacoes(service):
    resultado = service.users().messages().list(
        userId="me",
        q='is:unread subject:"Cadastro Portal Fake -"'
    ).execute()

    return resultado.get("messages", [])


def obter_mensagem(service, message_id):
    return service.users().messages().get(
        userId="me",
        id=message_id
    ).execute()


def obter_cabecalhos(mensagem):
    headers = mensagem["payload"].get("headers", [])

    dados = {}

    for header in headers:
        nome = header["name"].lower()

        if nome == "subject":
            dados["assunto"] = header["value"]

        elif nome == "from":
            dados["remetente"] = header["value"]

        elif nome == "date":
            dados["data"] = header["value"]

    return dados


def baixar_anexos(service, mensagem, pasta_destino):
    os.makedirs(pasta_destino, exist_ok=True)

    anexos = []

    def processar_partes(partes):
        for parte in partes:

            nome = parte.get("filename")

            if nome:
                body = parte.get("body", {})
                attachment_id = body.get("attachmentId")

                if attachment_id:
                    anexo = service.users().messages().attachments().get(
                        userId="me",
                        messageId=mensagem["id"],
                        id=attachment_id
                    ).execute()

                    dados = base64.urlsafe_b64decode(
                        anexo["data"]
                    )

                    caminho = os.path.join(
                        pasta_destino,
                        nome
                    )

                    with open(caminho, "wb") as arquivo:
                        arquivo.write(dados)

                    anexos.append(caminho)

            if parte.get("parts"):
                processar_partes(parte["parts"])

    payload = mensagem.get("payload", {})

    processar_partes(
        payload.get("parts", [])
    )

    return anexos


def marcar_como_lida(service, message_id):
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={
            "removeLabelIds": ["UNREAD"]
        }
    ).execute()


def enviar_email(service, destinatario, assunto, corpo):
    mensagem = MIMEText(
        corpo,
        "plain",
        "utf-8"
    )

    mensagem["to"] = destinatario
    mensagem["subject"] = assunto

    raw = base64.urlsafe_b64encode(
        mensagem.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={
            "raw": raw
        }
    ).execute()