from flask import Blueprint, render_template, request, session, redirect
from config import db
from modelos.plano import Plano
from dao.usuarioDAO import AlunoDAO
from dao.planoDAO import PlanoDAO

admin_bp = Blueprint('admin_blueprint', __name__)


@admin_bp.route("/admin")
def painel_adm():
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect('/login')

    lista_usuarios = AlunoDAO.listar_todos()
    lista_planos = PlanoDAO.listar_todos()

    return render_template("pgAdm.html", usuarios=lista_usuarios, planos=lista_planos)


@admin_bp.route("/admin/cadastrar_plano", methods=["POST"])
def cadastrar_plano():
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect('/login')

    nome_plano = request.form.get("nome_plano")
    preco_plano = request.form.get("preco_plano")
    duracao_dias = request.form.get("duracao_dias")  # Captura os dias

    if nome_plano and preco_plano and duracao_dias:
        novo_plano = Plano(nome_plano=nome_plano, preco_plano=float(preco_plano),duracao_dias=int(duracao_dias))
        PlanoDAO.salvar(novo_plano)

    return redirect('/admin')


@admin_bp.route("/admin/remover/<cpf>")
def remover_usuario(cpf):
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect('/login')

    AlunoDAO.atualizar_mensalidade(cpf, 'Inativo')


    return redirect('/admin')


@admin_bp.route("/admin/mensalidade/<cpf>/<status>")
def alterar_mensalidade(cpf, status):
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect('/login')

    AlunoDAO.atualizar_mensalidade(cpf, status)

    return redirect('/admin')


@admin_bp.route('/admin/remover_plano/<int:plano_id>')
def remover_plano(plano_id):
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect('/login')

    PlanoDAO.remover(plano_id)
    return redirect('/admin')


@admin_bp.route("/admin/usuario/<cpf>", methods=["GET", "POST"])
def detalhes_usuario(cpf):
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect('/login')

    # Busca o aluno pelo CPF
    aluno = AlunoDAO.buscar_por_usuario(cpf)

    if not aluno:
        return redirect('/admin')  # Se o aluno não existir, volta pro início

    # Se o administrador clicar no botão "Salvar Alterações"
    if request.method == "POST":
        dados_atualizados = {
            'nome': request.form.get("nome"),
            'login': request.form.get("login"),
            'datanascimento': request.form.get("datanascimento"),
            'email': request.form.get("email"),
            'telefone': request.form.get("telefone"),
            'mensalidade': request.form.get("mensalidade"),
            'plano_id': request.form.get("plano_id")
        }

        # Envia os dados para o DAO salvar no banco
        AlunoDAO.atualizar_dados_completos(cpf, dados_atualizados)

        # Redireciona de volta para a tela inicial de admin
        return redirect('/admin')

    # Se for apenas para visualizar a página (GET), carrega os planos e abre o HTML
    planos = PlanoDAO.listar_todos()
    return render_template("dt_aluno.html", u=aluno, planos=planos)