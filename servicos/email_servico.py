

import os
import smtplib
from datetime import date, datetime
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


def _formatar_rotulo_forma_pagamento(forma):
    if not forma:
        return "Não informada"
    mapa = {
        'pix': 'PIX',
        'dinheiro': 'Dinheiro',
        'cartao_credito': 'Cartão de Crédito',
        'cartao_debito': 'Cartão de Débito',
        'boleto': 'Boleto'
    }
    return mapa.get(str(forma).lower(), str(forma).replace('_', ' ').title())


def enviar_email_boas_vindas(destinatario, nome_usuario, login):
    """
    Dispara o e-mail de boas-vindas ao novo aluno cadastrado na academia.
    """
    primeiro_nome = nome_usuario.split()[0] if nome_usuario else "Aluno(a)"
    assunto = f"Bem-vindo(a) à Academia do Bitelo, {primeiro_nome}! 🏋️"

    texto = f"""Olá, {primeiro_nome}!

Seja muito bem-vindo(a) à Academia do Bitelo! Seu cadastro foi realizado com sucesso.

Seus dados de acesso:
- Usuário (Login): {login}
- E-mail: {destinatario}

Acesse o sistema para escolher seu plano de treino e acompanhar suas mensalidades.

Bons treinos e conte com a gente para alcançar seus objetivos!

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
    .badge {{ display: inline-block; background-color: #ef6c23; color: #ffffff; font-size: 11px; font-weight: 700; text-transform: uppercase; padding: 4px 10px; border-radius: 4px; letter-spacing: 1px; margin-bottom: 15px; }}
    .greeting {{ font-size: 20px; font-weight: bold; margin-bottom: 12px; color: #171b1e; }}
    .message {{ font-size: 14px; line-height: 1.6; color: #4a5259; margin-bottom: 20px; }}
    .info-box {{ background: #faf7f0; border-left: 4px solid #ef6c23; border-radius: 4px; padding: 16px; margin: 20px 0; }}
    .info-item {{ font-size: 13px; color: #2d3748; margin: 6px 0; }}
    .info-item strong {{ color: #171b1e; }}
    .footer {{ background: #ebe8df; padding: 16px; text-align: center; font-size: 11px; color: #687078; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Academia <span>do Bitelo</span></h1>
    </div>
    <div class="content">
        <div class="badge">Cadastro Concluído</div>
        <p class="greeting">Olá, {primeiro_nome}!</p>
        <p class="message">Seja muito bem-vindo(a) à <strong>Academia do Bitelo</strong>! Ficamos muito felizes em tê-lo(a) conosco em sua jornada de treinos e saúde.</p>
        
        <div class="info-box">
            <div class="info-item"><strong>Usuário / Login:</strong> {login}</div>
            <div class="info-item"><strong>E-mail Cadastrado:</strong> {destinatario}</div>
        </div>

        <p class="message">Você já pode fazer login na plataforma para consultar seus planos, acompanhar seus pagamentos e manter seus treinos em dia.</p>
        
        <p class="message" style="margin-bottom: 0; font-weight: 600; color: #ef6c23;">Foco nos treinos e conte sempre com nossa equipe!</p>
    </div>
    <div class="footer">
        © 2026 Academia do Bitelo • Todos os direitos reservados
    </div>
</div>
</body>
</html>
"""

    return enviar_email(destinatario, assunto, texto, html)


def enviar_aviso_alteracao_dados(destinatario, nome_usuario, detalhes="seus dados cadastrais e/ou credenciais"):
    """
    Dispara o e-mail de confirmação após a alteração de dados do perfil ou senha do aluno.
    """
    primeiro_nome = nome_usuario.split()[0] if nome_usuario else "Aluno(a)"
    assunto = "Segurança: Seus dados foram alterados - Academia do Bitelo"

    texto = f"""Olá, {primeiro_nome}!

Informamos que {detalhes} na sua conta da Academia do Bitelo foram atualizados com sucesso.

Se foi você quem realizou essa alteração, nenhuma ação adicional é necessária.

Caso NÃO tenha sido você, entre em contato imediatamente com a administração da academia para proteger seus dados e acesso.

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
    .badge {{ display: inline-block; background-color: #2b8a3e; color: #ffffff; font-size: 11px; font-weight: 700; text-transform: uppercase; padding: 4px 10px; border-radius: 4px; letter-spacing: 1px; margin-bottom: 15px; }}
    .greeting {{ font-size: 18px; font-weight: bold; margin-bottom: 12px; color: #171b1e; }}
    .message {{ font-size: 14px; line-height: 1.6; color: #4a5259; margin-bottom: 20px; }}
    .warning-box {{ background: #fff8e6; border: 1px solid #ffe08a; border-radius: 6px; padding: 14px; margin: 20px 0; font-size: 12px; color: #7a5800; line-height: 1.5; }}
    .footer {{ background: #ebe8df; padding: 16px; text-align: center; font-size: 11px; color: #687078; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Academia <span>do Bitelo</span></h1>
    </div>
    <div class="content">
        <div class="badge">Dados Atualizados</div>
        <p class="greeting">Olá, {primeiro_nome}!</p>
        <p class="message">Confirmamos que <strong>{detalhes}</strong> foram atualizados com sucesso no sistema da Academia do Bitelo.</p>
        
        <div class="warning-box">
            <strong>Aviso de segurança:</strong> Se você mesmo realizou essa alteração, seus dados já estão atualizados. Se você <strong>NÃO</strong> reconhece essa ação, procure a recepção da academia imediatamente para proteger seu acesso.
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


def enviar_notificacao_plano(destinatario, nome_usuario, nome_plano, data_vencimento=None):
    """
    Dispara o e-mail avisando o aluno que a administração alterou o seu plano de treino.
    """
    primeiro_nome = nome_usuario.split()[0] if nome_usuario else "Aluno(a)"
    assunto = "Seu plano foi atualizado - Academia do Bitelo"

    if isinstance(data_vencimento, (date, datetime)):
        vencimento_formatado = data_vencimento.strftime('%d/%m/%Y')
    elif isinstance(data_vencimento, str) and data_vencimento:
        vencimento_formatado = data_vencimento
    else:
        vencimento_formatado = None

    linha_vencimento_texto = f"\nVencimento: {vencimento_formatado}" if vencimento_formatado else ""
    linha_vencimento_html = (
        f'<div class="info-item"><strong>Vencimento:</strong> {vencimento_formatado}</div>'
        if vencimento_formatado else ""
    )

    texto = f"""Olá, {primeiro_nome}!

A administração da Academia do Bitelo atualizou o seu plano de treino.

Novo Plano: {nome_plano}{linha_vencimento_texto}

Se você não esperava essa alteração, entre em contato com a recepção da academia.

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
    .badge {{ display: inline-block; background-color: #ef6c23; color: #ffffff; font-size: 11px; font-weight: 700; text-transform: uppercase; padding: 4px 10px; border-radius: 4px; letter-spacing: 1px; margin-bottom: 15px; }}
    .greeting {{ font-size: 18px; font-weight: bold; margin-bottom: 12px; color: #171b1e; }}
    .message {{ font-size: 14px; line-height: 1.6; color: #4a5259; margin-bottom: 20px; }}
    .info-box {{ background: #faf7f0; border-left: 4px solid #ef6c23; border-radius: 4px; padding: 16px; margin: 20px 0; }}
    .info-item {{ font-size: 13px; color: #2d3748; margin: 6px 0; }}
    .info-item strong {{ color: #171b1e; }}
    .footer {{ background: #ebe8df; padding: 16px; text-align: center; font-size: 11px; color: #687078; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Academia <span>do Bitelo</span></h1>
    </div>
    <div class="content">
        <div class="badge">Plano Atualizado</div>
        <p class="greeting">Olá, {primeiro_nome}!</p>
        <p class="message">A administração da Academia do Bitelo atualizou o seu plano de treino.</p>

        <div class="info-box">
            <div class="info-item"><strong>Novo Plano:</strong> {nome_plano}</div>
            {linha_vencimento_html}
        </div>

        <p class="message">Se você não esperava essa alteração, entre em contato com a recepção da academia.</p>
    </div>
    <div class="footer">
        © 2026 Academia do Bitelo • Todos os direitos reservados
    </div>
</div>
</body>
</html>
"""

    return enviar_email(destinatario, assunto, texto, html)


def enviar_aviso_status_mensalidade(destinatario, nome_usuario, status):
    """
    Dispara o e-mail avisando o aluno sobre a alteração manual do status da mensalidade
    feita pelo admin (ex: Em Dia, Pendente, Inativo).
    """
    primeiro_nome = nome_usuario.split()[0] if nome_usuario else "Aluno(a)"
    status_label = status or "Atualizado"
    assunto = f"Situação da mensalidade: {status_label} - Academia do Bitelo"

    texto = f"""Olá, {primeiro_nome}!

A situação da sua mensalidade na Academia do Bitelo foi atualizada para: {status_label}.

Se tiver dúvidas sobre essa alteração, entre em contato com a recepção da academia.

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
    .badge {{ display: inline-block; background-color: #2b6cb0; color: #ffffff; font-size: 11px; font-weight: 700; text-transform: uppercase; padding: 4px 10px; border-radius: 4px; letter-spacing: 1px; margin-bottom: 15px; }}
    .greeting {{ font-size: 18px; font-weight: bold; margin-bottom: 12px; color: #171b1e; }}
    .message {{ font-size: 14px; line-height: 1.6; color: #4a5259; margin-bottom: 20px; }}
    .status-box {{ background: #faf7f0; border: 1px solid #e5e0d4; border-radius: 6px; padding: 16px; margin: 20px 0; text-align: center; }}
    .status-value {{ font-size: 18px; font-weight: 800; color: #171b1e; }}
    .footer {{ background: #ebe8df; padding: 16px; text-align: center; font-size: 11px; color: #687078; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Academia <span>do Bitelo</span></h1>
    </div>
    <div class="content">
        <div class="badge">Status Atualizado</div>
        <p class="greeting">Olá, {primeiro_nome}!</p>
        <p class="message">A situação da sua mensalidade na Academia do Bitelo foi atualizada:</p>

        <div class="status-box">
            <div class="status-value">{status_label}</div>
        </div>

        <p class="message">Se tiver dúvidas sobre essa alteração, entre em contato com a recepção da academia.</p>
    </div>
    <div class="footer">
        © 2026 Academia do Bitelo • Todos os direitos reservados
    </div>
</div>
</body>
</html>
"""

    return enviar_email(destinatario, assunto, texto, html)


def enviar_aviso_pagamento_atrasado(destinatario, nome_usuario, nome_plano, valor, vencimento=None):
    """
    Dispara o e-mail avisando o aluno que o pagamento da mensalidade está em atraso.
    """
    primeiro_nome = nome_usuario.split()[0] if nome_usuario else "Aluno(a)"
    assunto = "⚠️ Mensalidade em atraso - Academia do Bitelo"

    if isinstance(vencimento, (date, datetime)):
        vencimento_formatado = vencimento.strftime('%d/%m/%Y')
    elif isinstance(vencimento, str) and vencimento:
        vencimento_formatado = vencimento
    else:
        vencimento_formatado = None

    try:
        valor_float = float(valor)
        valor_str = f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        valor_str = str(valor)

    linha_vencimento_texto = f"\nVencimento: {vencimento_formatado}" if vencimento_formatado else ""
    linha_vencimento_html = (
        f"""<tr>
                    <td style="padding: 7px 0; color: #687078;">Vencimento:</td>
                    <td style="padding: 7px 0; font-weight: bold; text-align: right; color: #171b1e;">{vencimento_formatado}</td>
                </tr>"""
        if vencimento_formatado else ""
    )

    texto = f"""Olá, {primeiro_nome}!

Identificamos que a sua mensalidade da Academia do Bitelo está em atraso.

Plano: {nome_plano}
Valor: R$ {valor_str}{linha_vencimento_texto}

Para regularizar sua situação e manter seu acesso liberado, entre em contato com a recepção da academia o quanto antes.

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
    .badge-atraso {{ display: inline-block; background-color: #c53030; color: #ffffff; font-size: 12px; font-weight: 700; text-transform: uppercase; padding: 5px 12px; border-radius: 20px; letter-spacing: 1px; margin-bottom: 16px; }}
    .greeting {{ font-size: 18px; font-weight: bold; margin-bottom: 12px; color: #171b1e; }}
    .message {{ font-size: 14px; line-height: 1.6; color: #4a5259; margin-bottom: 20px; }}
    .receipt-card {{ background: #faf7f0; border: 1px solid #e5e0d4; border-radius: 6px; padding: 20px; margin: 20px 0; }}
    .receipt-title {{ font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #c53030; margin-bottom: 14px; border-bottom: 1px solid #e5e0d4; padding-bottom: 8px; }}
    .action-notice {{ background: #fdecea; border-left: 4px solid #c53030; padding: 12px 16px; border-radius: 4px; font-size: 13px; color: #7a1a1a; margin-top: 20px; }}
    .footer {{ background: #ebe8df; padding: 16px; text-align: center; font-size: 11px; color: #687078; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Academia <span>do Bitelo</span></h1>
    </div>
    <div class="content">
        <div class="badge-atraso">⚠ Mensalidade em atraso</div>
        <p class="greeting">Olá, {primeiro_nome}!</p>
        <p class="message">Identificamos que o pagamento abaixo está em atraso:</p>

        <div class="receipt-card">
            <div class="receipt-title">Mensalidade em Atraso</div>
            <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                <tr>
                    <td style="padding: 7px 0; color: #687078;">Plano:</td>
                    <td style="padding: 7px 0; font-weight: bold; text-align: right; color: #171b1e;">{nome_plano}</td>
                </tr>
                {linha_vencimento_html}
                <tr style="border-top: 1px solid #e0dbd0;">
                    <td style="padding: 10px 0 0 0; font-weight: bold; color: #171b1e;">Valor:</td>
                    <td style="padding: 10px 0 0 0; font-weight: 800; text-align: right; color: #c53030; font-size: 16px;">R$ {valor_str}</td>
                </tr>
            </table>
        </div>

        <div class="action-notice">
            <strong>Ação necessária:</strong> Regularize seu pagamento na recepção da academia para manter seu acesso liberado.
        </div>
    </div>
    <div class="footer">
        © 2026 Academia do Bitelo • Comprovante Gerado Automaticamente
    </div>
</div>
</body>
</html>
"""

    return enviar_email(destinatario, assunto, texto, html)


def enviar_confirmacao_pagamento(destinatario, nome_usuario, nome_plano, valor, forma_pagamento, data_pagamento=None):
    """
    Dispara o e-mail de recibo/confirmação de pagamento da mensalidade, informando o plano, valor e forma de pagamento.
    """
    primeiro_nome = nome_usuario.split()[0] if nome_usuario else "Aluno(a)"
    assunto = "✅ Mensalidade Confirmada - Academia do Bitelo"

    # Formata a data de pagamento
    if isinstance(data_pagamento, (date, datetime)):
        data_formatada = data_pagamento.strftime('%d/%m/%Y')
    elif isinstance(data_pagamento, str) and data_pagamento:
        data_formatada = data_pagamento
    else:
        data_formatada = date.today().strftime('%d/%m/%Y')

    # Formata o valor no padrão R$ XX,XX
    try:
        valor_float = float(valor)
        valor_str = f"{valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        valor_str = str(valor)

    forma_formatada = _formatar_rotulo_forma_pagamento(forma_pagamento)

    texto = f"""Olá, {primeiro_nome}!

Confirmamos o recebimento do pagamento da sua mensalidade na Academia do Bitelo.

Detalhes do Pagamento:
- Plano: {nome_plano}
- Valor Pago: R$ {valor_str}
- Forma de Pagamento: {forma_formatada}
- Data do Pagamento: {data_formatada}
- Status: PAGO (Em Dia)

Seu acesso à academia está 100% liberado. Obrigado pela preferência e ótimos treinos!

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
    .badge-pago {{ display: inline-block; background-color: #28a745; color: #ffffff; font-size: 12px; font-weight: 700; text-transform: uppercase; padding: 5px 12px; border-radius: 20px; letter-spacing: 1px; margin-bottom: 16px; }}
    .greeting {{ font-size: 18px; font-weight: bold; margin-bottom: 12px; color: #171b1e; }}
    .message {{ font-size: 14px; line-height: 1.6; color: #4a5259; margin-bottom: 20px; }}
    .receipt-card {{ background: #faf7f0; border: 1px solid #e5e0d4; border-radius: 6px; padding: 20px; margin: 20px 0; }}
    .receipt-title {{ font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #ef6c23; margin-bottom: 14px; border-bottom: 1px solid #e5e0d4; padding-bottom: 8px; }}
    .access-notice {{ background: #e8f5e9; border-left: 4px solid #28a745; padding: 12px 16px; border-radius: 4px; font-size: 13px; color: #1b5e20; margin-top: 20px; }}
    .footer {{ background: #ebe8df; padding: 16px; text-align: center; font-size: 11px; color: #687078; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Academia <span>do Bitelo</span></h1>
    </div>
    <div class="content">
        <div class="badge-pago">✔ Pagamento Confirmado</div>
        <p class="greeting">Olá, {primeiro_nome}!</p>
        <p class="message">Confirmamos o pagamento da sua mensalidade. Abaixo estão os dados do seu comprovante:</p>
        
        <div class="receipt-card">
            <div class="receipt-title">Comprovante de Mensalidade</div>
            <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                <tr>
                    <td style="padding: 7px 0; color: #687078;">Plano:</td>
                    <td style="padding: 7px 0; font-weight: bold; text-align: right; color: #171b1e;">{nome_plano}</td>
                </tr>
                <tr>
                    <td style="padding: 7px 0; color: #687078;">Forma de Pagamento:</td>
                    <td style="padding: 7px 0; font-weight: bold; text-align: right; color: #171b1e;">{forma_formatada}</td>
                </tr>
                <tr>
                    <td style="padding: 7px 0; color: #687078;">Data do Pagamento:</td>
                    <td style="padding: 7px 0; font-weight: bold; text-align: right; color: #171b1e;">{data_formatada}</td>
                </tr>
                <tr style="border-top: 1px solid #e0dbd0;">
                    <td style="padding: 10px 0 0 0; font-weight: bold; color: #171b1e;">Valor Pago:</td>
                    <td style="padding: 10px 0 0 0; font-weight: 800; text-align: right; color: #28a745; font-size: 16px;">R$ {valor_str}</td>
                </tr>
            </table>
        </div>

        <div class="access-notice">
            <strong>Acesso Liberado:</strong> Sua situação está <strong>Em Dia</strong>. Bons treinos!
        </div>
    </div>
    <div class="footer">
        © 2026 Academia do Bitelo • Comprovante Gerado Automaticamente
    </div>
</div>
</body>
</html>
"""

    return enviar_email(destinatario, assunto, texto, html)
