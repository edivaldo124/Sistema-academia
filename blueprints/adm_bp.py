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

    # PADRÃO DO PROFESSOR: Busca as listas usando as classes DAO estáticas
    lista_usuarios = AlunoDAO.listar_todos()
    lista_planos = PlanoDAO.listar_todos()

    return render_template("pgAdm.html", usuarios=lista_usuarios, planos=lista_planos)


@admin_bp.route("/admin/cadastrar_plano", methods=["POST"])
def cadastrar_plano():
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect('/login')

    nome_plano = request.form.get("nome_plano")
    preco_plano = request.form.get("preco_plano")

    if nome_plano and preco_plano:
        # PADRÃO DO PROFESSOR: Instancia o modelo e salva via DAO estático
        novo_plano = Plano(nome_plano=nome_plano, preco_plano=float(preco_plano))
        PlanoDAO.salvar(novo_plano)

    return redirect('/admin')


@admin_bp.route("/admin/remover/<cpf>")
def remover_usuario(cpf):
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect('/login')

    # TOTALMENTE ORM: Se você quiser inativar o aluno mudando o status
    AlunoDAO.atualizar_mensalidade(cpf, 'Inativo')

    # OBS: Se você preferir EXCLUIR ele definitivamente do banco de dados, descomente a linha abaixo:
    # AlunoDAO.remover(cpf)

    return redirect('/admin')


@admin_bp.route("/admin/mensalidade/<cpf>/<status>")
def alterar_mensalidade(cpf, status):
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect('/login')

    # TOTALMENTE ORM: Atualiza o status/mensalidade chamando a função estática do DAO
    AlunoDAO.atualizar_mensalidade(cpf, status)

    return redirect('/admin')


@admin_bp.route('/admin/remover_plano/<int:plano_id>')
def remover_plano(plano_id):
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect('/login')

    PlanoDAO.remover(plano_id)
    return redirect('/admin')