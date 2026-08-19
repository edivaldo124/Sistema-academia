

import os
import smtplib
from email.message import EmailMessage
import logging
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def obter_configuracoes_email():
    load_dotenv(override=True)
    remetente = (os.environ.get('EMAIL_REMETENTE') or os.environ.get('EMAIL_USER') or '').strip()
    senha = (os.environ.get('EMAIL_SENHA') or os.environ.get('EMAIL_PASSWORD') or '').strip()
    # Remove espaços internos comuns quando o usuário copia a Senha de Aplicativo do Google (ex: 'abcd efgh ijkl mnop')
    senha = senha.replace(' ', '')
    servidor_smtp = (os.environ.get('SMTP_SERVER') or 'smtp.gmail.com').strip()
    porta_smtp = int(os.environ.get('SMTP_PORT', 465))
    brevo_api_key = (os.environ.get('BREVO_API_KEY') or os.environ.get('SENDINBLUE_API_KEY') or '').strip()
    resend_api_key = (os.environ.get('RESEND_API_KEY') or '').strip()
    return remetente, senha, servidor_smtp, porta_smtp, brevo_api_key, resend_api_key


def _enviar_email_brevo(destinatario, assunto, conteudo_texto, conteudo_html, api_key, remetente):
    """Envia e-mail via API REST HTTPS da Brevo (antigo Sendinblue) - funciona no Render Free."""
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    payload = {
        "sender": {"name": "Academia do Bitelo", "email": remetente or "suporte@academiadobitelo.com"},
        "to": [{"email": destinatario}],
        "subject": assunto,
        "textContent": conteudo_texto,
    }
    if conteudo_html:
        payload["htmlContent"] = conteudo_html

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code in (200, 201, 202):
            return True, "E-mail enviado com sucesso."
        else:
            logger.error(f"Erro Brevo API ({resp.status_code}): {resp.text}")
            return False, f"Erro Brevo API ({resp.status_code}): {resp.text}"
    except Exception as e:
        logger.error(f"Exceção ao conectar à API Brevo: {e}")
        return False, f"Erro de conexão com Brevo: {str(e)}"


def _enviar_email_resend(destinatario, assunto, conteudo_texto, conteudo_html, api_key, remetente):
    """Envia e-mail via API REST HTTPS da Resend - funciona no Render Free."""
    url = "https://api.resend.com/emails"
    from_email = remetente if (remetente and not remetente.endswith('@gmail.com')) else "Academia do Bitelo <onboarding@resend.dev>"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": from_email,
        "to": [destinatario],
        "subject": assunto,
        "text": conteudo_texto,
    }
    if conteudo_html:
        payload["html"] = conteudo_html

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code in (200, 201):
            return True, "E-mail enviado com sucesso."
        else:
            logger.error(f"Erro Resend API ({resp.status_code}): {resp.text}")
            return False, f"Erro Resend API ({resp.status_code}): {resp.text}"
    except Exception as e:
        logger.error(f"Exceção ao conectar à API Resend: {e}")
        return False, f"Erro de conexão com Resend: {str(e)}"


def enviar_email(destinatario, assunto, conteudo_texto, conteudo_html=None):
    """
    Envia um e-mail utilizando Brevo API, Resend API ou smtplib tradicional (SMTP).
    """
    remetente, senha, servidor_smtp, porta_smtp, brevo_api_key, resend_api_key = obter_configuracoes_email()

    # 1. Se BREVO_API_KEY estiver configurada, envia via API HTTP da Brevo
    if brevo_api_key:
        return _enviar_email_brevo(destinatario, assunto, conteudo_texto, conteudo_html, brevo_api_key, remetente)

    # 2. Se RESEND_API_KEY estiver configurada, envia via API HTTP da Resend
    if resend_api_key:
        return _enviar_email_resend(destinatario, assunto, conteudo_texto, conteudo_html, resend_api_key, remetente)

    # 3. Fallback: Envio padrão via SMTP direto (smtplib)
    if not remetente or not senha or 'seu_email@' in remetente or senha == 'sua_senha_de_aplicativo_aqui':
        logger.warning("Credenciais de e-mail não configuradas ou com valores padrão no .env (EMAIL_REMETENTE e EMAIL_SENHA).")
        return False, "Configuração de e-mail ausente. Configure EMAIL_REMETENTE e EMAIL_SENHA ou BREVO_API_KEY no ambiente."

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = f"Academia do Bitelo <{remetente}>"
    msg['To'] = destinatario
    msg.set_content(conteudo_texto)

    if conteudo_html:
        msg.add_alternative(conteudo_html, subtype='html')

    try:
        if porta_smtp == 465:
            with smtplib.SMTP_SSL(servidor_smtp, porta_smtp, timeout=15) as smtp:
                smtp.login(remetente, senha)
                smtp.send_message(msg)
        else:
            with smtplib.SMTP(servidor_smtp, porta_smtp, timeout=15) as smtp:
                smtp.starttls()
                smtp.login(remetente, senha)
                smtp.send_message(msg)

        return True, "E-mail enviado com sucesso."
    except smtplib.SMTPAuthenticationError:
        logger.error("Erro de autenticação SMTP. Verifique o e-mail e a Senha de Aplicativo do Google.")
        return False, "Falha de autenticação no Gmail. Verifique se a Senha de Aplicativo foi gerada corretamente."
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {e}")
        return False, f"Erro ao enviar o e-mail: {str(e)}"


def enviar_codigo_verificacao(destinatario, nome_usuario, codigo, motivo="alteração de dados e credenciais"):
    """
    Formata e dispara o e-mail com o código de 6 dígitos para verificação de segurança.
    """
    primeiro_nome = nome_usuario.split()[0] if nome_usuario else "Aluno(a)"
    assunto = f"Código de Verificação: {codigo} - Academia do Bitelo"

    texto = f"""Olá, {primeiro_nome}!

Recebemos uma solicitação para {motivo} na sua conta da Academia do Bitelo.

Seu código de verificação é: {codigo}

Este código expira em 10 minutos.

Se você não fez essa solicitação, nenhuma ação é necessária e seus dados continuam seguros.

Atenciosamente,
Equipe Academia do Bitelo
"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f1e9; margin: 0; padding: 20px; color: #171b1e; }}
    .container {{ max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 6px; border: 1px solid #d9d8d2; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
    .header {{ background-color: #171b1e; padding: 24px; text-align: center; border-bottom: 4px solid #ef6c23; }}
    .header h1 {{ color: #ffffff; margin: 0; font-size: 22px; text-transform: uppercase; letter-spacing: 1px; }}
    .header h1 span {{ color: #ffc72c; }}
    .content {{ padding: 30px; }}
    .greeting {{ font-size: 18px; font-weight: bold; margin-bottom: 12px; }}
    .message {{ font-size: 14px; line-height: 1.6; color: #4a5259; margin-bottom: 24px; }}
    .code-box {{ background: #faf7f0; border: 2px dashed #ef6c23; border-radius: 6px; padding: 18px; text-align: center; margin: 24px 0; }}
    .code-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: #c94f0d; font-weight: 700; margin-bottom: 6px; }}
    .code {{ font-size: 36px; font-weight: 800; letter-spacing: 6px; color: #171b1e; font-family: monospace; }}
    .warning {{ font-size: 12px; color: #8a9197; line-height: 1.5; border-top: 1px solid #eee; padding-top: 18px; }}
    .footer {{ background: #ebe8df; padding: 16px; text-align: center; font-size: 11px; color: #687078; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Academia <span>do Bitelo</span></h1>
    </div>
    <div class="content">
        <p class="greeting">Olá, {primeiro_nome}!</p>
        <p class="message">Recebemos uma solicitação para <strong>{motivo}</strong> na sua conta. Para confirmar que é realmente você, utilize o código de segurança abaixo:</p>
        
        <div class="code-box">
            <div class="code-label">Seu código de verificação</div>
            <div class="code">{codigo}</div>
        </div>

        <p class="message">Este código é válido por <strong>10 minutos</strong>. Nunca compartilhe este código com outras pessoas.</p>
        
        <div class="warning">
            Se você não solicitou a alteração de seus dados, desconsidere este e-mail. Sua conta e credenciais permanecem protegidas.
        </div>
    </div>
    <div class="footer">
        © 2026 Academia do Bitelo • Segurança e Privacidade
    </div>
</div>
</body>
</html>
"""

    return enviar_email(destinatario, assunto, texto, html)
