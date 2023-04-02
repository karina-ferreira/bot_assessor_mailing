# Bot Assessor de Mailing 📩
Esse repositório contém o código para o trabalho final da disciplina de Algoritmos de Automação do Master em Jornalismo de Dados, Automação e Data Storytelling do Insper (2022-23). O robô consiste em um bot do Telegram que recebe como input um comentário sobre macroeconomia e a indicação de um mailing específico para ser enviado. Utilizando o SendGrid, o robô envia o comentário com uma mensagem personalizada a cada jornalista que faz parte de um dos cinco mailings específicos em um Google Sheets integrado ao código.  

### SetWebhook Telegram API
- colocar aqui porque será rodado apenas 1x

dados = {"url": "https://bot-assessor-mailing.onrender.com"}
resposta = requests.post(f"https://api.telegram.org/bot{FAZER UMA CHAVE}/setWebhook", data=dados)
print(resposta.text)
