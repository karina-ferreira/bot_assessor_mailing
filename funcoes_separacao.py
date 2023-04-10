import os

import gspread

from oauth2client.service_account import ServiceAccountCredentials

# ______________________________ variáveis de ambiente _________________________

GOOGLE_SHEETS_KEY = os.environ["GOOGLE_SHEETS_KEY"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"] 
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
  
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key(f'{GOOGLE_SHEETS_KEY}')
sheet_recebidas = planilha.worksheet("comentarios") 
sheet_mailing = planilha.worksheet("mailing") 

# ______________________________ funções ____________________________

def obter_mailing(lista_msg):
    global sheet_mailing
    categoria = lista_msg[0]
    mailing = sheet_mailing.get_all_records()
    emails = []
    
    for jornalista in mailing:
        print(jornalista['Código'])
        if str(jornalista['Código']) == str(categoria):
            emails.append(jornalista['E-mail'])
    return emails


def obter_titulo(lista_msg):   
    titulo = lista_msg[1]
    return titulo

  
def obter_comentario(lista_msg):   
    comentario = lista_msg[2]
    return comentario
