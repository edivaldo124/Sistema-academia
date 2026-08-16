import hmac
import secrets
from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Blueprint, abort, flash, redirect, render_template, request, session
from config import db
from modelos.plano import Plano
from dao.usuarioDAO import AlunoDAO
from dao.planoDAO import PlanoDAO
from dao.financeiroDAO import PagamentoDAO
from modelos.pagamento import Pagamento

admin_bp = Blueprint('admin_blueprint', __name__)


@admin_bp.route("/admin")
def painel_adm():
    if session.get('tipo_usuario') != 'admin' or session.get('usuario') != 'admin':
        return redirect('/login')

    lista_usuarios = AlunoDAO.listar_todos()
    lista_planos = PlanoDAO.listar_todos()
    token_exclusao = session.get('token_exclusao')

    if not token_exclusao:
        token_exclusao = secrets.token_urlsafe(32)
        session['token_exclusao'] = token_exclusao

    return render_template(
        "pgAdm.html",
        usuarios=lista_usuarios,
        planos=lista_planos,
        token_exclusao=token_exclusao
    )


@admin_bp.route("/admin/cadastrar_plano", methods=["POST"])
def cadastrar_plano():
    if session.get('tipo_usuario') != 'admin' or session.get('usuario') != 'admin':
        return redirect('/login')

    nome_plano = request.form.get("nome_plano")
    preco_plano = request.form.get("preco_plano")
    duracao_dias = request.form.get("duracao_dias")  # Captura os dias

    if nome_plano and preco_plano and duracao_dias:
        novo_plano = Plano(nome_plano=nome_plano, preco_plano=float(preco_plano),duracao_dias=int(duracao_dias))
        PlanoDAO.salvar(novo_plano)

    return redirect('/admin')

#


@admin_bp.route("/admin/remover/<int:aluno_id>", methods=["POST"])
def remover_usuario(aluno_id):
    if session.get('tipo_usuario') != 'admin' or session.get('usuario') != 'admin':
        return redirect('/login')

    token_formulario = request.form.get('token_exclusao', '')
    token_sessao = session.get('token_exclusao', '')

    if not token_sessao or not hmac.compare_digest(token_formulario, token_sessao):
        abort(400)

    resultado = AlunoDAO.remover(aluno_id)
    session['token_exclusao'] = secrets.token_urlsafe(32)

    if resultado is True:
        flash('Aluno removido com sucesso.', 'sucesso')
    elif resultado is None:
        flash('Aluno não encontrado.', 'erro')
    else:
        flash('Não foi possível remover o aluno porque existem dados vinculados.', 'erro')

    return redirect('/admin')





@admin_bp.route("/admin/mensalidade/<cpf>/<status>")
def alterar_mensalidade(cpf, status):
    if session.get('tipo_usuario') != 'admin' or session.get('usuario') != 'admin':
        return redirect('/login')

    AlunoDAO.atualizar_mensalidade(cpf, status)

    return redirect('/admin')


@admin_bp.route('/admin/remover_plano/<int:plano_id>')
def remover_plano(plano_id):
    if session.get('tipo_usuario') != 'admin' or session.get('usuario') != 'admin':
        return redirect('/login')

    PlanoDAO.remover(plano_id)
    return redirect('/admin')


@admin_bp.route("/admin/usuario/<cpf>", methods=["GET", "POST"])
def detalhes_usuario(cpf):
    if session.get('tipo_usuario') != 'admin' or session.get('usuario') != 'admin':
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_usuario(cpf)

    if not aluno:
        return redirect('/admin')

    if request.method == "POST":
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

        AlunoDAO.atualizar_dados_completos(cpf, dados_atualizados)

        return redirect('/admin')


    planos = PlanoDAO.listar_todos()
    pagamentos = PagamentoDAO.listar_por_aluno(aluno.id)
    return render_template("dt_aluno.html", u=aluno, planos=planos, pagamentos=pagamentos)


@admin_bp.route("/admin/usuario/<cpf>/pagamentos", methods=["POST"])
def cadastrar_pagamento(cpf):
    if session.get('tipo_usuario') != 'admin' or session.get('usuario') != 'admin':
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_usuario(cpf)
    plano = PlanoDAO.buscar_por_id(request.form.get('plano_id'))

    try:
        valor = Decimal((request.form.get('valor') or '').replace(',', '.'))
        vencimento = date.fromisoformat(request.form.get('vencimento') or '')
    except (InvalidOperation, ValueError):
        flash('Valor ou vencimento inválido.', 'erro')
        return redirect(f'/admin/usuario/{cpf}')

    status = request.form.get('status', 'pendente')
    forma_pagamento = request.form.get('forma_pagamento') or None
    data_pagamento_texto = request.form.get('data_pagamento') or None

    if not aluno or not plano or valor <= 0 or status not in PagamentoDAO.STATUS_VALIDOS:
        flash('Não foi possível cadastrar a mensalidade. Verifique os dados.', 'erro')
        return redirect(f'/admin/usuario/{cpf}')

    try:
        data_pagamento = date.fromisoformat(data_pagamento_texto) if data_pagamento_texto else None
    except ValueError:
        flash('Data de pagamento inválida.', 'erro')
        return redirect(f'/admin/usuario/{cpf}')

    if status == 'pago' and not forma_pagamento:
        flash('Informe a forma de pagamento para uma mensalidade paga.', 'erro')
        return redirect(f'/admin/usuario/{cpf}')
    if forma_pagamento and forma_pagamento not in PagamentoDAO.FORMAS_VALIDAS:
        flash('Forma de pagamento inválida.', 'erro')
        return redirect(f'/admin/usuario/{cpf}')

    pagamento = Pagamento(
        aluno_id=aluno.id,
        plano_id=plano.id,
        valor=valor,
        vencimento=vencimento,
        status=status,
        forma_pagamento=forma_pagamento if status == 'pago' else None,
        data_pagamento=(data_pagamento or date.today()) if status == 'pago' else None,
    )
    PagamentoDAO.salvar(pagamento)
    aluno.mensalidade = 'Em Dia' if status == 'pago' else status.capitalize()
    db.session.commit()
    flash('Mensalidade cadastrada com sucesso.', 'sucesso')
    return redirect(f'/admin/usuario/{cpf}')


@admin_bp.route("/admin/pagamentos/<int:pagamento_id>/status", methods=["POST"])
def atualizar_status_pagamento(pagamento_id):
    if session.get('tipo_usuario') != 'admin' or session.get('usuario') != 'admin':
        return redirect('/login')

    pagamento = PagamentoDAO.buscar_por_id(pagamento_id)
    if not pagamento:
        flash('Pagamento não encontrado.', 'erro')
        return redirect('/admin')

    status = request.form.get('status', '')
    forma_pagamento = request.form.get('forma_pagamento') or None
    if status == 'pago' and not forma_pagamento:
        flash('Informe a forma de pagamento.', 'erro')
        return redirect(f'/admin/usuario/{pagamento.aluno.cpf}')
    if forma_pagamento and forma_pagamento not in PagamentoDAO.FORMAS_VALIDAS:
        flash('Forma de pagamento inválida.', 'erro')
        return redirect(f'/admin/usuario/{pagamento.aluno.cpf}')

    if not PagamentoDAO.atualizar_status(pagamento, status, forma_pagamento):
        flash('Status inválido.', 'erro')
    else:
        pagamento.aluno.mensalidade = 'Em Dia' if status == 'pago' else status.capitalize()
        db.session.commit()
        flash('Status do pagamento atualizado.', 'sucesso')

    return redirect(f'/admin/usuario/{pagamento.aluno.cpf}')
