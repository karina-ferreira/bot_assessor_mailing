# Bot Assessor de Mailing 📩
Esse repositório contém o código do trabalho final da disciplina de Algoritmos de Automação do Master em Jornalismo de Dados, Automação e Data Storytelling do Insper (2022-23). O robô consiste em um bot do Telegram que recebe como input um comentário sobre macroeconomia e a indicação de um mailing específico para ser enviado. Utilizando o SendGrid, o robô envia o comentário com uma mensagem personalizada a cada jornalista que faz parte de um dos seis mailings específicos em um Google Sheets integrado ao código.  

### SetWebhook Telegram API
Para automatizar o código, utilizamos o webhook, recurso que possibilita que um sistema se comunique com outro e ambos troquem dados em tempo real e sem a nossa interferência. Nesse caso, a troca acontece sempre que o bot recebe uma nova mensagem. Por meio de uma página criada com Flask no Render, as funcionalidades ficam disponíveis online. O seguinte trecho deve ser rodado apenas uma vez para a integração ser feita: 
```
import requests

dados = {"url": "https://bot-assessor-mailing.onrender.com/telegram-bot"}
resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/setWebhook", data=dados)
print(resposta.text)
```
### Conversar com o Bot Assessor de Mailing 
O [Bot Assessor de Mailing](https://t.me/assessor_mailing_bot) é um canal particular que serve como ferramenta de automatização de um trabalho cotidiano da autora desse repositório. Somente usuários específicos têm permissão para usá-lo. 
