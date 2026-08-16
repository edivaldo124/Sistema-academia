from flask import Blueprint, render_template, request, session, redirect
from sqlalchemy.exc import IntegrityError
from config import db
from modelos.usuario import Aluno
from dao.usuarioDAO import AlunoDAO
from dao.planoDAO import PlanoDAO
from dao.financeiroDAO import PagamentoDAO

auth_bp = Blueprint('auth', __name__)

MSG_ERRO = 'Erro: Credenciais incorretas!'


@auth_bp.route("/login", methods=["GET", "POST"])
def pagina_login():
    if request.method == "POST":
        login = (request.form.get("loginusuario") or "").strip()
        senha = request.form.get("senhausuario") or ""

        if login == "admin" and senha == "admin":
            # Remove qualquer sessao anterior para evitar fixacao de sessao.
            session.clear()
            session['usuario'] = "admin"
            session['tipo_usuario'] = "admin"
            session.permanent = True
            return redirect('/admin')

        aluno = AlunoDAO.autenticar(login, senha)
        if aluno:
            session.clear()
            # O ID nao muda se o aluno editar o login, email ou nome.
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
    if session.get('tipo_usuario') != 'aluno' or not session.get('aluno_id'):
        return redirect('/login')

    aluno_dados = db.session.get(Aluno, session['aluno_id'])

    if not aluno_dados:
        session.clear()
        return redirect('/logout')

    if request.method == "POST":
        plano_id_escolhido = request.form.get("plano")
        if plano_id_escolhido and plano_id_escolhido != "Nenhum":
            aluno_dados.plano_id = int(plano_id_escolhido)
            db.session.commit()

    lista_planos = PlanoDAO.listar_todos()
    pagamentos = PagamentoDAO.listar_por_aluno(aluno_dados.id)

    return render_template("pgUsuario.html", usuario=aluno_dados, planos=lista_planos, pagamentos=pagamentos)

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
