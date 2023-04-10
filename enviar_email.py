import os
import sendgrid

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

# ______________________________ variáveis de ambiente _________________________

SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY_SITE"] 

# ______________________________ função ________________________________________

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
