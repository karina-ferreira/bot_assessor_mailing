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
