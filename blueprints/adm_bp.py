import logging
import hmac
import secrets
from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, session
from config import db
from modelos.plano import Plano
from dao.usuarioDAO import AlunoDAO
from dao.planoDAO import PlanoDAO
from dao.financeiroDAO import PagamentoDAO
from modelos.pagamento import Pagamento
from servicos.formatacao import formatar_telefone
from servicos.email_servico import (
    enviar_confirmacao_pagamento,
    enviar_notificacao_plano,
    enviar_aviso_status_mensalidade,
    enviar_aviso_pagamento_atrasado,
    enviar_recado_admin,
)

logger = logging.getLogger(__name__)

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


@admin_bp.route("/admin/recados", methods=["POST"])
def enviar_recado():
    if session.get('tipo_usuario') != 'admin' or session.get('usuario') != 'admin':
        return redirect('/login')

    assunto = (request.form.get('assunto') or '').strip()
    mensagem = (request.form.get('mensagem') or '').strip()

    if not mensagem:
        flash('Escreva uma mensagem antes de enviar o recado.', 'erro')
        return redirect('/admin')

    alunos = [a for a in AlunoDAO.listar_todos() if a.email]
    enviados = 0
    falhas = 0

    for aluno in alunos:
        try:
            sucesso, _ = enviar_recado_admin(
                destinatario=aluno.email,
                nome_usuario=aluno.nome,
                assunto=assunto,
                mensagem=mensagem
            )
            if sucesso:
                enviados += 1
            else:
                falhas += 1
        except Exception as e:
            falhas += 1
            logger.error(f"Erro ao enviar recado para {aluno.email}: {e}")

    if enviados:
        resumo = f'Recado enviado para {enviados} aluno(s).'
        if falhas:
            resumo += f' Falhou para {falhas}.'
        flash(resumo, 'sucesso')
    else:
        flash('Não foi possível enviar o recado para nenhum aluno.', 'erro')

    return redirect('/admin')


@admin_bp.route("/admin/cadastrar_plano", methods=["POST"])
def cadastrar_plano():
    if session.get('tipo_usuario') != 'admin' or session.get('usuario') != 'admin':
        return redirect('/login')

    nome_plano = request.form.get("nome_plano")
    preco_plano = request.form.get("preco_plano")
    duracao_dias = request.form.get("duracao_dias")  

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

    aluno = AlunoDAO.buscar_por_usuario(cpf)
    AlunoDAO.atualizar_mensalidade(cpf, status)

    if aluno and aluno.email:
        try:
            enviar_aviso_status_mensalidade(
                destinatario=aluno.email,
                nome_usuario=aluno.nome,
                status=status
            )
        except Exception as e:
            logger.error(f"Erro ao enviar aviso de status da mensalidade por e-mail: {e}")

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
            'telefone': formatar_telefone(request.form.get("telefone")),
            'mensalidade': request.form.get("mensalidade"),
            'plano_id': request.form.get("plano_id"),
            'descricao': request.form.get('descricao')
        }

        plano_id_anterior = aluno.plano_id

        AlunoDAO.atualizar_dados_completos(cpf, dados_atualizados)

        # Dispara aviso por e-mail quando o admin muda o plano do aluno
        if aluno.plano_id and aluno.plano_id != plano_id_anterior and aluno.email:
            try:
                plano_novo = PlanoDAO.buscar_por_id(aluno.plano_id)
                enviar_notificacao_plano(
                    destinatario=aluno.email,
                    nome_usuario=aluno.nome,
                    nome_plano=plano_novo.nome_plano if plano_novo else "Plano de Treino",
                    data_vencimento=aluno.data_vencimento
                )
            except Exception as e:
                logger.error(f"Erro ao enviar notificação de novo plano por e-mail: {e}")

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

    valor = request.form.get('valor')
    vencimento = request.form.get('vencimento')
    status = request.form.get('status')
    forma_pagamento = request.form.get('forma_pagamento')
    data_pagamento = request.form.get('data_pagamento')

    if aluno and plano and valor and vencimento:
        novo_pagamento = Pagamento(
            aluno_id=aluno.id,
            plano_id=plano.id,
            valor=float(valor),
            vencimento=date.fromisoformat(vencimento),
            status=status,
            forma_pagamento=forma_pagamento if forma_pagamento else None,
            data_pagamento=date.fromisoformat(data_pagamento) if data_pagamento else None
        )

        PagamentoDAO.salvar(novo_pagamento)
        aluno.mensalidade = 'Em Dia' if status == 'pago' else status.capitalize()
        db.session.commit()

        if status == 'pago' and aluno.email:
            try:
                enviar_confirmacao_pagamento(
                    destinatario=aluno.email,
                    nome_usuario=aluno.nome,
                    nome_plano=plano.nome_plano if plano else "Plano de Treino",
                    valor=float(valor),
                    forma_pagamento=forma_pagamento or "Não informada",
                    data_pagamento=novo_pagamento.data_pagamento or novo_pagamento.vencimento or date.today()
                )
            except Exception as e:
                logger.error(f"Erro ao enviar recibo de pagamento por e-mail: {e}")
        elif status == 'atrasado' and aluno.email:
            try:
                enviar_aviso_pagamento_atrasado(
                    destinatario=aluno.email,
                    nome_usuario=aluno.nome,
                    nome_plano=plano.nome_plano if plano else "Plano de Treino",
                    valor=float(valor),
                    vencimento=novo_pagamento.vencimento
                )
            except Exception as e:
                logger.error(f"Erro ao enviar aviso de atraso por e-mail: {e}")

    return redirect(f'/admin/usuario/{cpf}')


@admin_bp.route("/admin/pagamentos/<int:pagamento_id>/status", methods=["POST"])
def atualizar_status_pagamento(pagamento_id):
    if session.get('tipo_usuario') != 'admin' or session.get('usuario') != 'admin':
        return redirect('/login')

    pagamento = PagamentoDAO.buscar_por_id(pagamento_id)
    if not pagamento:
        flash('Pagamento não encontrado.', 'erro')
        return redirect('/admin')

    status = request.form.get('status')
    forma_pagamento = request.form.get('forma_pagamento')

    PagamentoDAO.atualizar_status(pagamento_id, status, forma_pagamento)
    pagamento.aluno.mensalidade = 'Em Dia' if status == 'pago' else status.capitalize()
    db.session.commit()

    if status == 'pago' and pagamento.aluno and pagamento.aluno.email:
        try:
            plano_nome = pagamento.plano.nome_plano if pagamento.plano else "Plano de Treino"
            forma = forma_pagamento if forma_pagamento else pagamento.forma_pagamento
            data_pg = pagamento.data_pagamento if pagamento.data_pagamento else date.today()
            enviar_confirmacao_pagamento(
                destinatario=pagamento.aluno.email,
                nome_usuario=pagamento.aluno.nome,
                nome_plano=plano_nome,
                valor=pagamento.valor,
                forma_pagamento=forma or "Não informada",
                data_pagamento=data_pg
            )
        except Exception as e:
            logger.error(f"Erro ao enviar recibo de pagamento por e-mail: {e}")
    elif status == 'atrasado' and pagamento.aluno and pagamento.aluno.email:
        try:
            plano_nome = pagamento.plano.nome_plano if pagamento.plano else "Plano de Treino"
            enviar_aviso_pagamento_atrasado(
                destinatario=pagamento.aluno.email,
                nome_usuario=pagamento.aluno.nome,
                nome_plano=plano_nome,
                valor=pagamento.valor,
                vencimento=pagamento.vencimento
            )
        except Exception as e:
            logger.error(f"Erro ao enviar aviso de atraso por e-mail: {e}")

    return redirect(f'/admin/usuario/{pagamento.aluno.cpf}')
