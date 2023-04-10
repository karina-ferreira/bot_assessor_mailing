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

import obter_info_msg
import enviar_email
import funcoes_separacao

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

# ______________________________ site __________________________________________

app = Flask(__name__)

@app.route("/")
def index():
  return "Esse é o site de teste"

# ______________________________ bot (FUNCIONANDO) _____________________________

@app.route("/telegram-bot", methods = ["POST"])
def telegram_bot():
  
    update = request.json 

# Dados da mensagem
    update_id = update['update_id']
    first_name = update['message']['from']['first_name']
    last_name = update['message']['from']['last_name']
    user_name = update['message']['from']['username']
    sender_id = update['message']['from']['id']
    chat_id = update['message']['chat']['id']
    message = update["message"]["text"]
    date = datetime.fromtimestamp(update['message']['date']).date()
    time = datetime.fromtimestamp(update['message']['date']).time()
    
# Funções
    lista_msg = obter_info_msg.obter_info_msg(message)
    emails = funcoes_separacao.obter_mailing(lista_msg)
    titulo = funcoes_separacao.obter_titulo(lista_msg)
    comentario = funcoes_separacao.obter_comentario(lista_msg)
    resultado_envios = enviar_email.enviar_email(emails, titulo, comentario)

# Define qual será a resposta
    texto_resposta = ""
    if message == "/start":
        texto_resposta = "Este é um robô privado para envio de conteúdo sensível."
    else:
        texto_resposta = resultado_envios
        
# Define a lista de usuários permitidos
    usuarios_permitidos = ["kuaraina", "kuaraina2", "turicas"]    

# Verifica se o usuário está na lista de usuários permitidos e define resposta para não permitidos
    if not user_name or user_name not in usuarios_permitidos:
        texto_resposta = "Você não está autorizado a usar este bot."
    
# Envia a resposta 

    nova_mensagem = {"chat_id": chat_id, "text": texto_resposta} 
    requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)

    return "ok"
