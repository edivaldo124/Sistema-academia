from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from config import db
from modelos.plano import Plano
from modelos.usuario import Aluno
from dao.usuarioDAO import AlunoDAO
from dao.planoDAO import PlanoDAO
from servicos.notificacoes_email import enviar_plano_selecionado, enviar_status_mensalidade

admin_bp = Blueprint('admin_blueprint', __name__)
STATUS_VALIDOS = {'Pendente', 'Em Dia', 'Inativo'}


def avisar_status_atualizado(aluno):
    if enviar_status_mensalidade(aluno):
        flash('Status atualizado e aviso enviado por e-mail.', 'sucesso')
    else:
        flash('Status atualizado, mas não foi possível enviar o aviso por e-mail.', 'aviso')


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

#


@admin_bp.route("/admin/remover/<cpf>")
def remover_usuario(cpf):
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect('/login')

    aluno = Aluno.query.filter_by(cpf=cpf).first()
    if aluno and AlunoDAO.atualizar_mensalidade(cpf, 'Inativo'):
        avisar_status_atualizado(aluno)
    else:
        flash('Aluno não encontrado.', 'erro')

    return redirect('/admin')





@admin_bp.route("/admin/mensalidade/<cpf>/<status>")
def alterar_mensalidade(cpf, status):
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect('/login')

    if status not in STATUS_VALIDOS:
        flash('Status de mensalidade inválido.', 'erro')
        return redirect('/admin')

    aluno = Aluno.query.filter_by(cpf=cpf).first()
    if aluno and AlunoDAO.atualizar_mensalidade(cpf, status):
        avisar_status_atualizado(aluno)
    else:
        flash('Aluno não encontrado.', 'erro')

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

    aluno = AlunoDAO.buscar_por_usuario(cpf)

    if not aluno:
        return redirect('/admin')

    if request.method == "POST":
        status_anterior = aluno.mensalidade
        plano_anterior = aluno.plano_id

        dados_atualizados = {
            'nome': request.form.get("nome"),
            'login': request.form.get("login"),
            'datanascimento': request.form.get("datanascimento"),
            'email': request.form.get("email"),
            'telefone': request.form.get("telefone"),
            'mensalidade': request.form.get("mensalidade"),
            'plano_id': request.form.get("plano_id"),
            'descricao': request.form.get('descricao')
        }

        if dados_atualizados['mensalidade'] not in STATUS_VALIDOS:
            flash('Status de mensalidade inválido.', 'erro')
            return redirect(url_for('admin_blueprint.detalhes_usuario', cpf=cpf))

        plano_id = dados_atualizados['plano_id']
        plano = None
        if plano_id and plano_id != 'Nenhum':
            try:
                plano = PlanoDAO.buscar_por_id(int(plano_id))
            except (TypeError, ValueError):
                plano = None

            if not plano:
                flash('Plano inválido.', 'erro')
                return redirect(url_for('admin_blueprint.detalhes_usuario', cpf=cpf))

        if not AlunoDAO.atualizar_dados_completos(cpf, dados_atualizados):
            flash('Não foi possível atualizar o aluno.', 'erro')
            return redirect('/admin')

        if aluno.mensalidade != status_anterior:
            enviar_status_mensalidade(aluno)

        if aluno.plano_id != plano_anterior and plano:
            enviar_plano_selecionado(aluno, plano)

        flash('Dados do aluno atualizados.', 'sucesso')

        return redirect('/admin')


    planos = PlanoDAO.listar_todos()
    return render_template("dt_aluno.html", u=aluno, planos=planos)
