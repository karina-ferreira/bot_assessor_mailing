import os

import datetime
import getpass
import gspread
import json
import pandas as pd
import requests
import sendgrid
import time

from flask import Flask, request
from io import StringIO 
from oauth2client.service_account import ServiceAccountCredentials
from sendgrid.helpers.mail import Mail, Email, To, Content


# ______________________________ site

app = Flask(__name__)

@app.route("/")
def index():
  return "Esse é o site do Bot Assessor de Mailing. Para conferir a documentação acesse: https://github.com/karina-ferreira/bot_assessor_mailing"
