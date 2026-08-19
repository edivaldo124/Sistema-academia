import logging
import secrets
import time
from flask import Blueprint, render_template, request, session, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError
from config import db
from modelos.usuario import Aluno
from dao.usuarioDAO import AlunoDAO
from dao.planoDAO import PlanoDAO
from dao.financeiroDAO import PagamentoDAO
from servicos.formatacao import formatar_cpf, formatar_telefone, somente_digitos, variantes_cpf
from servicos.email_servico import (
    enviar_codigo_verificacao,
    enviar_email_boas_vindas,
    enviar_aviso_alteracao_dados
)

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

MSG_ERRO = 'Erro: Credenciais incorretas!'


def mascarar_email(email):
    if not email or '@' not in email:
        return email or ''
    partes = email.split('@')
    nome_usuario = partes[0]
    dominio = partes[1]
    if len(nome_usuario) <= 2:
        mascarado = nome_usuario[0] + '***'
    else:
        mascarado = nome_usuario[:2] + '***' + nome_usuario[-1]
    return f"{mascarado}@{dominio}"


@auth_bp.route("/login", methods=["GET", "POST"])
def pagina_login():
    if request.method == "POST":
        login = (request.form.get("loginusuario") or "").strip()
        senha = request.form.get("senhausuario") or ""

        if login == "admin" and senha == "admin":
            session.clear()
            session['usuario'] = "admin"
            session['tipo_usuario'] = "admin"
            session.permanent = True
            return redirect('/admin')

        aluno = AlunoDAO.autenticar(login, senha)
        if aluno:
            session.clear()
            session['usuario'] = aluno.login
            session['aluno_id'] = aluno.id
            session['tipo_usuario'] = "aluno"
            session.permanent = True
            return redirect('/perfil')

        return render_template('login.html', msg=MSG_ERRO)

    return render_template("login.html")


@auth_bp.route("/cadastrar", methods=["GET", "POST"])
def pagina_cadastro():
    if request.method == "POST":
        nome = (request.form.get("nomeusuario") or "").strip()
        login = (request.form.get("loginusuario") or "").strip()
        datanascimento = (request.form.get("dataNascimento") or "").strip()
        cpf = formatar_cpf(request.form.get("cpfusuario"))
        senha = request.form.get("senhausuario") or ""
        email = (request.form.get("emailusuario") or "").strip().lower()
        telefone = formatar_telefone(request.form.get("telefoneusuario"))
        descricao = (request.form.get("descricaousuario") or "").strip()

        if not all([nome, login, datanascimento, cpf, senha.strip(), email, telefone]):
            return render_template("cadastro.html", erro="Erro: Preencha todos os campos obrigatórios!")

        if len(somente_digitos(cpf)) != 11:
            return render_template("cadastro.html", erro="Erro: Informe um CPF com 11 dígitos!")

        if Aluno.query.filter(Aluno.cpf.in_(variantes_cpf(cpf))).first():
            return render_template("cadastro.html", erro="Erro: Este CPF já está cadastrado!")

        if Aluno.query.filter_by(login=login).first():
            return render_template("cadastro.html", erro="Erro: Este usuário já está cadastrado!")

        if Aluno.query.filter_by(email=email).first():
            return render_template("cadastro.html", erro="Erro: Este e-mail já está cadastrado!")

        novo_aluno = Aluno(
            nome=nome,
            login=login,
            datanascimento=datanascimento,
            cpf=cpf,
            email=email,
            telefone=telefone,
            senha=senha,
            descricao=descricao
        )

        try:
            AlunoDAO.salvar(novo_aluno)
        except IntegrityError:
            db.session.rollback()
            return render_template("cadastro.html", erro="Erro: Não foi possível cadastrar. Verifique se os dados já estão em uso.")

        # Envia e-mail de boas-vindas para o aluno recém-cadastrado
        try:
            enviar_email_boas_vindas(
                destinatario=novo_aluno.email,
                nome_usuario=novo_aluno.nome,
                login=novo_aluno.login
            )
        except Exception as e:
            logger.error(f"Erro ao enviar e-mail de boas-vindas: {e}")

        return redirect('/login')

    return render_template("cadastro.html")


@auth_bp.route("/perfil", methods=["GET", "POST"])
def pagina_perfil():
    if session.get('tipo_usuario') != 'aluno' or not session.get('aluno_id'):
        return redirect('/login')

    aluno_dados = AlunoDAO.buscar_por_id(session['aluno_id'])

    if not aluno_dados:
        session.clear()
        return redirect('/logout')

    if request.method == "POST":
        plano_id_escolhido = request.form.get("plano")
        if plano_id_escolhido and plano_id_escolhido != "Nenhum":
            aluno_dados.plano_id = int(plano_id_escolhido)
            db.session.commit()
            flash("Plano atualizado com sucesso!", "sucesso")

    lista_planos = PlanoDAO.listar_todos()
    pagamentos = PagamentoDAO.listar_por_aluno(aluno_dados.id)

    return render_template("pgUsuario.html", usuario=aluno_dados, planos=lista_planos, pagamentos=pagamentos)


@auth_bp.route("/perfil/editar", methods=["GET", "POST"])
def editar_perfil():
    if session.get('tipo_usuario') != 'aluno' or not session.get('aluno_id'):
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_id(session['aluno_id'])
    if not aluno:
        session.clear()
        return redirect('/logout')

    if request.method == "POST":
        nome = (request.form.get("nome") or "").strip()
        login = (request.form.get("login") or "").strip()
        datanascimento = (request.form.get("datanascimento") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        telefone = formatar_telefone(request.form.get("telefone"))
        descricao = (request.form.get("descricao") or "").strip()

        senha_atual = request.form.get("senha_atual") or ""
        nova_senha = request.form.get("nova_senha") or ""
        confirmar_senha = request.form.get("confirmar_senha") or ""

        # Validações básicas
        if not all([nome, login, datanascimento, email, telefone]):
            return render_template("editar_perfil.html", usuario=aluno, erro="Preencha todos os campos obrigatórios.")

        if AlunoDAO.login_em_uso_por_outro(login, aluno.id):
            return render_template("editar_perfil.html", usuario=aluno, erro="Este nome de usuário já está sendo usado por outro aluno.")

        if AlunoDAO.email_em_uso_por_outro(email, aluno.id):
            return render_template("editar_perfil.html", usuario=aluno, erro="Este e-mail já está cadastrado por outro aluno.")

        # Se o usuário informou nova senha, validar senha atual e confirmação
        if nova_senha:
            if not senha_atual:
                return render_template("editar_perfil.html", usuario=aluno, erro="Informe sua senha atual para definir uma nova senha.")
            if senha_atual != aluno.senha:
                return render_template("editar_perfil.html", usuario=aluno, erro="A senha atual informada está incorreta.")
            if len(nova_senha) < 4:
                return render_template("editar_perfil.html", usuario=aluno, erro="A nova senha deve ter no mínimo 4 caracteres.")
            if nova_senha != confirmar_senha:
                return render_template("editar_perfil.html", usuario=aluno, erro="A nova senha e a confirmação de senha não coincidem.")

        # Geração do código de verificação de 6 dígitos
        codigo_verificacao = f"{secrets.randbelow(900000) + 100000}"

        # Guarda dados na sessão temporária
        session['pendente_alteracao'] = {
            'aluno_id': aluno.id,
            'codigo': codigo_verificacao,
            'expira_em': time.time() + 600,  # 10 minutos de validade
            'email_destino': aluno.email,
            'dados': {
                'nome': nome,
                'login': login,
                'datanascimento': datanascimento,
                'email': email,
                'telefone': telefone,
                'descricao': descricao,
                'nova_senha': nova_senha if nova_senha else None
            }
        }

        # Envia e-mail de verificação para o Gmail cadastrado
        sucesso_envio, msg_envio = enviar_codigo_verificacao(
            destinatario=aluno.email,
            nome_usuario=aluno.nome,
            codigo=codigo_verificacao,
            motivo="alteração de dados cadastrais e credenciais"
        )

        if not sucesso_envio:
            flash(f"Atenção: Não foi possível enviar o e-mail automaticamente ({msg_envio}). Por favor verifique as configurações no .env.", "erro")

        return redirect(url_for('auth.verificar_codigo'))

    return render_template("editar_perfil.html", usuario=aluno)


@auth_bp.route("/perfil/verificar_codigo", methods=["GET", "POST"])
def verificar_codigo():
    if session.get('tipo_usuario') != 'aluno' or not session.get('aluno_id'):
        return redirect('/login')

    pendente = session.get('pendente_alteracao')
    if not pendente:
        flash("Nenhuma alteração pendente de confirmação.", "erro")
        return redirect('/perfil')

    aluno = AlunoDAO.buscar_por_id(session['aluno_id'])
    email_mascarado = mascarar_email(pendente.get('email_destino', aluno.email if aluno else ''))

    if request.method == "POST":
        codigo_digitado = (request.form.get("codigo") or "").strip()

        if not codigo_digitado:
            return render_template("verificar_codigo.html", email_mascarado=email_mascarado, erro="Informe o código de verificação recebido.")

        # Verifica se o código expirou
        if time.time() > pendente.get('expira_em', 0):
            return render_template("verificar_codigo.html", email_mascarado=email_mascarado, erro="O código de verificação expirou. Clique em reenviar código.")

        # Verifica se o código confere
        if codigo_digitado != pendente.get('codigo'):
            return render_template("verificar_codigo.html", email_mascarado=email_mascarado, erro="Código de verificação incorreto. Verifique o seu e-mail e tente novamente.")

        # Código válido: aplicar alterações no banco de dados
        sucesso = AlunoDAO.atualizar_credenciais_aluno(pendente['aluno_id'], pendente['dados'])

        if sucesso:
            novo_login = pendente['dados']['login']
            session['usuario'] = novo_login
            
            # Envia e-mail notificando a alteração de dados com sucesso
            try:
                dest_email = pendente['dados'].get('email') or pendente.get('email_destino')
                detalhe = "sua nova senha e dados de acesso" if pendente['dados'].get('nova_senha') else "seus dados de perfil"
                enviar_aviso_alteracao_dados(
                    destinatario=dest_email,
                    nome_usuario=pendente['dados'].get('nome', aluno.nome if aluno else "Aluno"),
                    detalhes=detalhe
                )
            except Exception as e:
                logger.error(f"Erro ao disparar aviso de alteração de dados: {e}")

            session.pop('pendente_alteracao', None)
            flash("Suas credenciais e dados cadastrais foram atualizados com sucesso!", "sucesso")
            return redirect('/perfil')
        else:
            return render_template("verificar_codigo.html", email_mascarado=email_mascarado, erro="Erro ao salvar alterações no banco de dados. Tente novamente.")

    return render_template("verificar_codigo.html", email_mascarado=email_mascarado)


@auth_bp.route("/perfil/reenviar_codigo", methods=["POST"])
def reenviar_codigo():
    if session.get('tipo_usuario') != 'aluno' or not session.get('aluno_id'):
        return redirect('/login')

    pendente = session.get('pendente_alteracao')
    if not pendente:
        flash("Nenhuma alteração pendente.", "erro")
        return redirect('/perfil')

    aluno = AlunoDAO.buscar_por_id(session['aluno_id'])
    novo_codigo = f"{secrets.randbelow(900000) + 100000}"

    pendente['codigo'] = novo_codigo
    pendente['expira_em'] = time.time() + 600
    session['pendente_alteracao'] = pendente

    sucesso_envio, msg_envio = enviar_codigo_verificacao(
        destinatario=aluno.email,
        nome_usuario=aluno.nome,
        codigo=novo_codigo,
        motivo="alteração de dados cadastrais e credenciais"
    )

    if sucesso_envio:
        flash("Um novo código de verificação foi enviado para seu e-mail.", "sucesso")
    else:
        flash(f"Não foi possível enviar o e-mail ({msg_envio}). Verifique o arquivo .env.", "erro")

    return redirect(url_for('auth.verificar_codigo'))


@auth_bp.route("/perfil/cancelar_alteracao", methods=["GET", "POST"])
def cancelar_alteracao():
    session.pop('pendente_alteracao', None)
    flash("Alteração de dados cancelada.", "info")
    return redirect('/perfil')


@auth_bp.route("/recuperar_senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        cpf = formatar_cpf(request.form.get("cpf"))
        email = (request.form.get("email") or "").strip().lower()
        nova_senha = request.form.get("nova_senha")

        aluno = Aluno.query.filter(Aluno.cpf.in_(variantes_cpf(cpf)), Aluno.email == email).first()

        if aluno:
            aluno.senha = nova_senha
            db.session.commit()

            # Envia e-mail de aviso de alteração de senha
            try:
                enviar_aviso_alteracao_dados(
                    destinatario=aluno.email,
                    nome_usuario=aluno.nome,
                    detalhes="sua senha de acesso (via recuperação de senha)"
                )
            except Exception as e:
                logger.error(f"Erro ao disparar aviso de alteração de senha: {e}")

            return render_template("login.html", msg="Senha alterada com sucesso! Faça login.")
        else:
            return render_template("recuperar.html", erro="CPF ou E-mail incorretos!")

    return render_template("recuperar.html")
