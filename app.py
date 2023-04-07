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

# ______________________________ bot (teste quase completo) ___________________________________________ 

@app.route("/telegram-bot", methods = ["POST"])
def telegram_bot():
    mensagens = []
  
    if request.method == 'POST':
        update = request.get_json()

        # Defina a lista de usuários permitidos
        usuarios_permitidos = []
        #usuarios_permitidos = ["kuaraina", "kuaraina2"]

        # Loop para processar cada atualização recebida
        for cada_update in update:
            update_id = cada_update["update_id"]

            # Verifica se o usuário é permitido
            if "username" in cada_update["message"]["from"] and cada_update["message"]["from"]["username"] in usuarios_permitidos:
                # Extrai dados para mostrar mensagem recebida
                first_name = cada_update["message"]["from"]["first_name"]
                sender_id = cada_update["message"]["from"]["id"]
                if "text" not in cada_update["message"]:
                    continue  # Essa mensagem não é um texto!
                message = cada_update["message"]["text"]
                chat_id = cada_update["message"]["chat"]["id"]
                datahora = str(datetime.datetime.fromtimestamp(cada_update["message"]["date"]))
                username = cada_update["message"]["from"]["username"] if "username" in cada_update["message"]["from"] else "[não definido]"
                print(f"[{datahora}] Nova mensagem de {first_name} @{username} ({chat_id}): {message}")
                mensagens.append([datahora, "recebida", username, first_name, chat_id, message])

                # Define qual será a resposta e envia
                if message == "/start":
                    texto_resposta = "Este é um robô privado para envio de conteúdo sensível."
                else:
                    texto_resposta = "texto resposta" #**************************** AQUI ENTRA A INTEGRAÇÃO COM GSHEETS E SENDGRID???????
                nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
                requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
                mensagens.append([datahora, "enviada", username, first_name, chat_id, texto_resposta])
            else:
                texto_resposta_negado = "Você não tem permissão para utilizar esse serviço."
                # Se o usuário não for permitido, pula para a próxima atualização
                continue
