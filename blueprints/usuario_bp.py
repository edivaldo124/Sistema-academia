from flask import Blueprint, render_template, request, session
from modelos.usuario import Usuario
from dao.usuarioDAO import dao_usuario

auth_bp = Blueprint('auth', __name__)

msg = 'Erro: Usuário ou senha incorretos!'
@auth_bp.route("/login", methods=["GET", "POST"])
def pagina_login():
    if request.method == "POST":
        login = request.form.get("loginusuario")
        senha = request.form.get("senhausuario")

        usuario = dao_usuario.autenticar(login, senha)
        if usuario:
            session['usuario_logado'] = usuario.login

            if usuario.login == 'admin':
                lista_usuarios = dao_usuario.listar_todos()
                lista_planos = dao_usuario.listar_planos()
                return render_template('pgAdm.html', usuarios=lista_usuarios, planos=lista_planos)

            lista_planos = dao_usuario.listar_planos()
            return render_template('pgUsuario.html', usuario=usuario, planos=lista_planos)


        return render_template('login.html', msg=msg)
    return render_template("login.html")


@auth_bp.route("/cadastrar", methods=["GET", "POST"])
def pagina_cadastro():
    if request.method == "POST":
        nome = request.form.get("nomeusuario")
        login = request.form.get("loginusuario")
        senha = request.form.get("senhausuario")
        email = request.form.get("emailusuario")
        telefone = request.form.get("telefoneusuario")
        cpf = request.form.get("cpfusuario")

        if nome and login and senha and email and telefone and cpf:
            novo_user = Usuario(nome, login, senha, email, telefone, cpf)
            if dao_usuario.salvar(novo_user):
                return render_template('login.html')
            return "Erro: Esse nome de usuário já existe!"
        return "Erro: Todos os campos são obrigatórios!"
    return render_template("cadastro.html")


@auth_bp.route("/perfil", methods=["GET", "POST"])
def pagina_perfil():
    if 'usuario_logado' not in session:
        return render_template('login.html')

    if request.method == "POST":
        plano_escolhido = request.form.get("plano")
        dao_usuario.atualizar_plano(session['usuario_logado'], plano_escolhido)

    usuario = dao_usuario.buscar_por_login(session['usuario_logado'])
    lista_planos = dao_usuario.listar_planos()
    return render_template("pgUsuario.html", usuario=usuario, planos=lista_planos)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return render_template('index.html')

#@auth_bp.route("/logout2")
#def logout():
    session.clear()
    return render_template('login.html')