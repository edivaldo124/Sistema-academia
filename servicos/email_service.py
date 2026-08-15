import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr

from flask import current_app


def email_configurado():
    """Informa se há dados suficientes para tentar um envio."""
    remetente = current_app.config.get('MAIL_DEFAULT_SENDER')
    usuario = current_app.config.get('MAIL_USERNAME')
    senha = current_app.config.get('MAIL_PASSWORD')

    autenticacao_completa = bool(usuario and senha)
    sem_autenticacao = not usuario and not senha

    return bool(remetente and (autenticacao_completa or sem_autenticacao))


def enviar_email(destinatario, assunto, mensagem, mensagem_html=None):
    """Envia um e-mail e devolve True ou False sem interromper a operação principal."""
    if not destinatario or not email_configurado():
        current_app.logger.warning(
            'E-mail não enviado: configure MAIL_DEFAULT_SENDER, '
            'MAIL_USERNAME e MAIL_PASSWORD.'
        )
        return False

    servidor_smtp = current_app.config['MAIL_SERVER']
    porta = current_app.config['MAIL_PORT']
    usar_tls = current_app.config['MAIL_USE_TLS']
    usuario = current_app.config.get('MAIL_USERNAME')
    senha = current_app.config.get('MAIL_PASSWORD', '').replace(' ', '')
    remetente = current_app.config['MAIL_DEFAULT_SENDER']
    nome_remetente = current_app.config.get('MAIL_SENDER_NAME', 'Academia')
    tempo_limite = current_app.config.get('MAIL_TIMEOUT', 10)

    try:
        email = EmailMessage()
        email['Subject'] = assunto
        email['From'] = formataddr((nome_remetente, remetente))
        email['To'] = destinatario
        email.set_content(mensagem)

        if mensagem_html:
            email.add_alternative(mensagem_html, subtype='html')

        with smtplib.SMTP(servidor_smtp, porta, timeout=tempo_limite) as smtp:
            smtp.ehlo()

            if usar_tls:
                smtp.starttls(context=ssl.create_default_context())
                smtp.ehlo()

            if usuario and senha:
                smtp.login(usuario, senha)

            smtp.send_message(email)

        return True
    except (OSError, smtplib.SMTPException, ValueError):
        current_app.logger.exception('Falha ao enviar e-mail pelo servidor SMTP.')
        return False
