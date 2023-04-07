import os

import datetime
import gspread
import json
import requests
import sendgrid
import time

from flask import Flask, request
from io import StringIO 
from oauth2client.service_account import ServiceAccountCredentials
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# ______________________________ variáveis de ambiente _________________________

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"] 
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
  return "Esse é o site do Bot Assessor de Mailing. Para conferir a documentação acesse: https://github.com/karina-ferreira/bot_assessor_mailing"

# ______________________________ bot (teste 2 refazendo o código) ____________________

@app.route("/telegram-bot", methods = ["POST"])
def telegram_bot():
    mensagens = []
  
    update = request.json 

    # dados da mensagem
    update_id = update['update_id']
    first_name = update['message']['from']['first_name']
    last_name = update['message']['from']['last_name']
    user_name = update['message']['from']['username']
    sender_id = update['message']['from']['id']
    chat_id = update['message']['chat']['id']
    date = datetime.fromtimestamp(update['message']['date']).date().strftime('%d/%m/%Y')
    time = datetime.fromtimestamp(update['message']['date']).time()

    # Define qual será a resposta e envia
    if message == "/start":
        texto_resposta = "Este é um robô privado para envio de conteúdo sensível."
    else:
        texto_resposta = "estou em fase de testes!" #**************************** AQUI ENTRA A INTEGRAÇÃO COM GSHEETS E SENDGRID / fazer funções
        nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
        requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
        mensagens.append([datahora, "enviada", username, first_name, chat_id, texto_resposta])

    print(resposta.text)
    return "ok"
