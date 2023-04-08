categoria = 0
titulo = 0
comentario = 0

def obter_info_msg(message):

    global categoria
    global titulo
    global comentario
    partes_mensagem = message.split("/")
    if len(partes_mensagem) == 3:
        categoria, titulo, comentario = partes_mensagem
        return categoria, titulo, comentario, None
    else:
        texto_resposta = "A mensagem deve ter o seguinte formato: 'número da categoria (1-6)/título do comentário/comentário em si', separado por barras."
        return None, None, None, texto_resposta
