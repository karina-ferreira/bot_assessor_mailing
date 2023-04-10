# pega a mensagem recebida pelo bot, divide em 3 partes e retorna uma lista
def obter_info_msg(message):
    message = message.split("/")

    if len(message) == 3:
        lista_msg = message
        return lista_msg
    else:
        texto_resposta = "A mensagem deve ter o seguinte formato: 'número da categoria (1-6)/título do comentário/comentário em si', separado por barras."
        return None, None, None, texto_resposta
