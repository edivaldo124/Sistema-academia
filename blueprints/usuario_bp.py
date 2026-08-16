from flask import Blueprint, render_template, request, session, redirect
from sqlalchemy.exc import IntegrityError
from config import db
from modelos.usuario import Aluno
from dao.usuarioDAO import AlunoDAO
from dao.planoDAO import PlanoDAO

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

        return redirect('/login')

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
        if plano_id_escolhido and plano_id_escolhido != "Nenhum":
            aluno_dados.plano_id = int(plano_id_escolhido)
            db.session.commit()

    lista_planos = PlanoDAO.listar_todos()

    return render_template("pgUsuario.html", usuario=aluno_dados, planos=lista_planos)

@auth_bp.route("/recuperar_senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        nova_senha = request.form.get("nova_senha")

        from modelos.usuario import Aluno
        from config import db
        aluno = Aluno.query.filter_by(cpf=cpf, email=email).first()

        if aluno:
            aluno.senha = nova_senha
            db.session.commit()
            return render_template("login.html", msg="Senha alterada com sucesso! Faça login.")
        else:
            return render_template("recuperar.html", erro="CPF ou E-mail incorretos!")

    return render_template("recuperar.html")

