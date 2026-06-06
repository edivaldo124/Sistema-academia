from flask import Blueprint, render_template, request, session, redirect
from config import db
from modelos import usuario
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

        # Login do Administrador
        if login == "admin" and senha == "admin":
            session['usuario'] = "admin"
            return redirect('/admin')

        # PADRÃO DO PROFESSOR: Chama o método estático do DAO
        aluno = AlunoDAO.autenticar(login, senha)
        if aluno:
            session['usuario'] = login
            return redirect('/perfil')

        return render_template('login.html', msg=MSG_ERRO)

    return render_template("login.html")


@auth_bp.route("/cadastrar", methods=["GET", "POST"])
def pagina_cadastro():
    if request.method == "POST":
        nome = request.form.get("nomeusuario")
        login = request.form.get("loginusuario")
        datanascimento = request.form.get("dataNascimento")
        cpf = request.form.get("cpfusuario")
        senha = request.form.get("senhausuario")
        email = request.form.get("emailusuario")
        telefone = request.form.get("telefoneusuario")

        if nome and login and cpf and senha and email and telefone:
            # PADRÃO DO PROFESSOR: Verifica se já existe antes de salvar
            aluno_existente = AlunoDAO.buscar_por_usuario(cpf)
            if aluno_existente:
                return render_template("cadastro.html", erro="Erro: Este CPF já está cadastrado!")

            # PADRÃO DO PROFESSOR: Cria o objeto Aluno usando o construtor __init__
            novo_aluno = Aluno(nome=nome, login=login,datanascimento=datanascimento,cpf=cpf, email=email, telefone=telefone, senha=senha)

            # Salva usando o método estático do DAO
            AlunoDAO.salvar(novo_aluno)
            return redirect('/login')

        return render_template("cadastro.html", erro="Erro: Todos os campos são obrigatórios!")

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
            # Com o ORM, podemos alterar a propriedade diretamente no objeto carregado!
            aluno_dados.plano_id = int(plano_id_escolhido)
            db.session.commit()  # Grava a alteração do plano no banco de dados

    # Carrega a lista de planos para o <select> do HTML
    lista_planos = PlanoDAO.listar_todos()

    return render_template("pgUsuario.html", usuario=aluno_dados, planos=lista_planos)

@auth_bp.route("/recuperar_senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        nova_senha = request.form.get("nova_senha")

        # Procura o aluno pelo CPF e Email juntos
        from modelos.usuario import Aluno
        from config import db
        aluno = Aluno.query.filter_by(cpf=cpf, email=email).first()

        if aluno:
            aluno.senha = nova_senha # Atualiza a senha
            db.session.commit()
            return render_template("login.html", msg="Senha alterada com sucesso! Faça login.")
        else:
            return render_template("recuperar.html", erro="CPF ou E-mail incorretos!")

    return render_template("recuperar.html")


