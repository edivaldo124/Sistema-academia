from urllib.parse import urljoin

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError

from config import db
from modelos.usuario import Aluno
from dao.usuarioDAO import AlunoDAO
from dao.planoDAO import PlanoDAO
from servicos.email_service import email_configurado
from servicos.notificacoes_email import (
    enviar_boas_vindas,
    enviar_link_recuperacao,
    enviar_plano_selecionado,
    enviar_senha_alterada,
)
from servicos.recuperacao_senha import buscar_aluno_pelo_token, gerar_token_recuperacao

auth_bp = Blueprint('auth', __name__)

MSG_ERRO = 'Erro: Credenciais incorretas!'


@auth_bp.route("/login", methods=["GET", "POST"])
def pagina_login():
    if request.method == "POST":
        login = request.form.get("loginusuario")
        senha = request.form.get("senhausuario")

        if login == "admin" and senha == "admin":
            session['usuario'] = "admin"
            return redirect('/admin')

        aluno = AlunoDAO.autenticar(login, senha)
        if aluno:
            session['usuario'] = login
            return redirect('/perfil')

        return render_template('login.html', msg=MSG_ERRO)

    return render_template("login.html")


@auth_bp.route("/cadastrar", methods=["GET", "POST"])
def pagina_cadastro():
    if request.method == "POST":
        nome = (request.form.get("nomeusuario") or "").strip()
        login = (request.form.get("loginusuario") or "").strip()
        datanascimento = (request.form.get("dataNascimento") or "").strip()
        cpf = (request.form.get("cpfusuario") or "").strip()
        senha = request.form.get("senhausuario") or ""
        email = (request.form.get("emailusuario") or "").strip().lower()
        telefone = (request.form.get("telefoneusuario") or "").strip()
        descricao = (request.form.get("descricaousuario") or "").strip()

        if not all([nome, login, datanascimento, cpf, senha.strip(), email, telefone]):
            return render_template("cadastro.html", erro="Erro: Preencha todos os campos obrigatórios!")

        if len(senha) < 8:
            return render_template("cadastro.html", erro="Erro: A senha deve ter pelo menos 8 caracteres!")

        if Aluno.query.filter_by(cpf=cpf).first():
            return render_template("cadastro.html", erro="Erro: Este CPF já está cadastrado!")

        if Aluno.query.filter_by(login=login).first():
            return render_template("cadastro.html", erro="Erro: Este usuário já está cadastrado!")

        if Aluno.query.filter_by(email=email).first():
            return render_template("cadastro.html", erro="Erro: Este e-mail já está cadastrado!")

        novo_aluno = Aluno(nome=nome, login=login, datanascimento=datanascimento, cpf=cpf, email=email, telefone=telefone, senha=senha, descricao=descricao)

        try:
            AlunoDAO.salvar(novo_aluno)
        except IntegrityError:
            db.session.rollback()
            return render_template("cadastro.html", erro="Erro: Não foi possível cadastrar. Verifique se os dados já estão em uso.")

        if enviar_boas_vindas(novo_aluno):
            flash('Cadastro realizado! Enviamos uma confirmação para o seu e-mail.', 'sucesso')
        else:
            flash('Cadastro realizado, mas não foi possível enviar o e-mail de confirmação.', 'aviso')

        return redirect(url_for('auth.pagina_login'))

    return render_template("cadastro.html")


@auth_bp.route("/perfil", methods=["GET", "POST"])
def pagina_perfil():
    if 'usuario' not in session:
        return redirect('/login')

    aluno_dados = AlunoDAO.buscar_por_usuario(session['usuario'])

    if not aluno_dados:
        return redirect('/logout')

    if request.method == "POST":
        plano_id_escolhido = request.form.get("plano")
        try:
            plano_id = int(plano_id_escolhido)
        except (TypeError, ValueError):
            flash('Escolha um plano válido.', 'erro')
            return redirect(url_for('auth.pagina_perfil'))

        plano = PlanoDAO.buscar_por_id(plano_id)
        if not plano:
            flash('O plano escolhido não existe mais.', 'erro')
            return redirect(url_for('auth.pagina_perfil'))

        if aluno_dados.plano_id == plano.id:
            flash('Esse já é o seu plano atual.', 'aviso')
            return redirect(url_for('auth.pagina_perfil'))

        aluno_dados.plano_id = plano.id
        db.session.commit()

        if enviar_plano_selecionado(aluno_dados, plano):
            flash('Plano selecionado! Enviamos os detalhes para o seu e-mail.', 'sucesso')
        else:
            flash('Plano selecionado, mas não foi possível enviar o aviso por e-mail.', 'aviso')

        return redirect(url_for('auth.pagina_perfil'))

    lista_planos = PlanoDAO.listar_todos()

    return render_template("pgUsuario.html", usuario=aluno_dados, planos=lista_planos)

@auth_bp.route("/recuperar_senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        cpf = (request.form.get("cpf") or "").strip()
        email = (request.form.get("email") or "").strip().lower()

        if not cpf or not email:
            return render_template("recuperar.html", erro="Preencha o CPF e o e-mail.")

        if not email_configurado():
            return render_template(
                "recuperar.html",
                erro="O envio de e-mail ainda não está configurado no servidor."
            )

        if not current_app.config.get('SECRET_KEY_CONFIGURADA', True):
            return render_template(
                "recuperar.html",
                erro="Configure uma SECRET_KEY segura antes de usar a recuperação de senha."
            )

        aluno = Aluno.query.filter_by(cpf=cpf, email=email).first()

        if aluno:
            token = gerar_token_recuperacao(aluno)
            caminho = url_for('auth.redefinir_senha', token=token)
            endereco_publico = current_app.config.get('APP_BASE_URL')
            link = (
                urljoin(f'{endereco_publico}/', caminho.lstrip('/'))
                if endereco_publico
                else url_for('auth.redefinir_senha', token=token, _external=True)
            )
            segundos = current_app.config.get('RESET_TOKEN_MAX_AGE', 1800)
            minutos = max(1, int(segundos / 60))
            enviar_link_recuperacao(aluno, link, minutos)

        return render_template(
            "recuperar.html",
            mensagem="Se os dados estiverem corretos, você receberá um link para redefinir a senha."
        )

    return render_template("recuperar.html")


@auth_bp.route("/redefinir_senha/<token>", methods=["GET", "POST"])
def redefinir_senha(token):
    aluno = buscar_aluno_pelo_token(token)
    if not aluno:
        return render_template(
            "recuperar.html",
            erro="Este link é inválido, expirou ou já foi utilizado."
        ), 400

    if request.method == "POST":
        nova_senha = request.form.get("nova_senha") or ""
        confirmar_senha = request.form.get("confirmar_senha") or ""

        if len(nova_senha) < 8:
            return render_template(
                "redefinir_senha.html",
                token=token,
                erro="A senha deve ter pelo menos 8 caracteres."
            )

        if nova_senha != confirmar_senha:
            return render_template(
                "redefinir_senha.html",
                token=token,
                erro="As senhas digitadas não são iguais."
            )

        aluno.definir_senha(nova_senha)
        db.session.commit()
        enviar_senha_alterada(aluno)

        flash('Senha alterada com sucesso! Faça login.', 'sucesso')
        return redirect(url_for('auth.pagina_login'))

    return render_template("redefinir_senha.html", token=token)
