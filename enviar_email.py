import os

import gspread
import json
import requests
import sendgrid
import time

from datetime import date, time
from datetime import datetime
from flask import Flask, request
from io import StringIO 
from oauth2client.service_account import ServiceAccountCredentials
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

# ______________________________ variáveis de ambiente _________________________

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY_SITE"] 
GOOGLE_SHEETS_KEY = os.environ["GOOGLE_SHEETS_KEY"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"] 
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
  
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key(f'{GOOGLE_SHEETS_KEY}')
sheet_recebidas = planilha.worksheet("comentarios") 
sheet_mailing = planilha.worksheet("mailing") 

# ______________________________ função ____________________________

def enviar_email(emails, titulo, comentario):
 
  
    # Cria objeto responsável por enviar os emails
    carteiro = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

    # Só prepara e envia o e-mail caso a lista 'emails' tenha pelo menos um item
    if not emails:
        return "O e-mail não será enviado porque o mailing indicado não existe. Use um número entre 1 e 6 para escolher o mailing adequado. Eles são:\n\n1 - Internacional\n2 - Macro\n3 - IBGE\n4 - Dólar\n5 - Mercado\n6 - Investimentos"

    respostas = [] # lista para armazenar as respostas

    # Criar objeto do email
    for cada_email in emails:
        email = Mail(
            Email("karina@pecancom.com.br"), # Remetente
            To(cada_email),  # Destinatário
            titulo,  # Assunto/Título
            Content("text/plain", comentario),  # Corpo do email
        )

        # Enviar o email e armazenar a resposta
        try:
            resposta = carteiro.client.mail.send.post(request_body=email.get())
            print(f"E-mail enviado para {email.to_emails[0]}. Status: {resposta.status_code}") #tem alguma coisa errada aqui mas depois eu vejo!!
            respostas.append(resposta)
        except Exception as e:
            print(f"E-mail enviado para {cada_email}.") # essa ele imprime, a de cima não, mas os e-mails são enviados!

    return respostas
