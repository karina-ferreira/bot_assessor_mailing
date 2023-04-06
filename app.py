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

# ______________________________ bot ___________________________________________

@app.route("/telegram-bot", methods=['POST'])
def telegram_bot():
  mensagens = []

  update = request.json
  
  if request.method == 'POST':
     update = request.get_json()
    
  update_id = update['update_id']
  first_name = update['message']['from']['first_name']
  last_name = update['message']['from']['last_name']
  user_name = update['message']['from']['username']
  sender_id = update['message']['from']['id']
  date = datetime.fromtimestamp(update['message']['date']).date()
  time = datetime.fromtimestamp(update['message']['date']).time()
  chat_id = update['message']['chat']['id']
  
  try:
      message = update['message']['text']
  except KeyError:
      print("erro")
      message=''

  #return chat_id, texto
  
  if "username" in update["message"]["from"]:
    username = f' @{update["message"]["from"]["username"]}'
  else:
    username = ""

  
  if message == "oi":
     texto_resposta = f"teste"
  elif message == "1":
     texto_resposta = f"teste 2"
  else:
     texto_resposta = f"teste 3"

  nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
  resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data = nova_mensagem)
  return "ok"
