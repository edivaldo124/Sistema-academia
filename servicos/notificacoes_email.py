from flask import current_app

from servicos.email_service import enviar_email


def _nome_academia():
    return current_app.config.get('MAIL_SENDER_NAME', 'Academia')


def enviar_boas_vindas(aluno):
    mensagem = f"""Olá, {aluno.nome}!

Seu cadastro na {_nome_academia()} foi realizado com sucesso.
Seu usuário de acesso é: {aluno.login}

Por segurança, nunca enviaremos sua senha por e-mail.
"""
    return enviar_email(aluno.email, 'Cadastro realizado com sucesso', mensagem)


def enviar_plano_selecionado(aluno, plano):
    preco = f'{plano.preco_plano:.2f}'.replace('.', ',')
    mensagem = f"""Olá, {aluno.nome}!

O plano {plano.nome_plano} foi selecionado no seu perfil.
Valor: R$ {preco}
Duração: {plano.duracao_dias} dias

Este aviso confirma a seleção do plano, não a confirmação do pagamento.
"""
    return enviar_email(aluno.email, 'Plano selecionado', mensagem)


def enviar_status_mensalidade(aluno):
    mensagem = f"""Olá, {aluno.nome}!

O status da sua mensalidade foi atualizado para: {aluno.mensalidade}.

Em caso de dúvida, entre em contato com a {_nome_academia()}.
"""
    return enviar_email(aluno.email, 'Atualização da mensalidade', mensagem)


def enviar_link_recuperacao(aluno, link, minutos_validade):
    mensagem = f"""Olá, {aluno.nome}!

Recebemos uma solicitação para redefinir sua senha.
Use o link abaixo dentro de {minutos_validade} minutos:

{link}

Se você não solicitou a alteração, ignore esta mensagem.
"""
    return enviar_email(aluno.email, 'Recuperação de senha', mensagem)


def enviar_senha_alterada(aluno):
    mensagem = f"""Olá, {aluno.nome}!

Sua senha foi alterada com sucesso.
Se você não reconhece essa alteração, entre em contato com a {_nome_academia()}.
"""
    return enviar_email(aluno.email, 'Senha alterada', mensagem)
