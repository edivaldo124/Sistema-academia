import logging
from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, session

from dao.usuarioDAO import AlunoDAO
from dao.professorDAO import ProfessorDAO
from dao.avaliacaoDAO import AvaliacaoDAO
from modelos.avaliacao import Avaliacao

logger = logging.getLogger(__name__)

professor_bp = Blueprint('professor_blueprint', __name__)


def _guard():
    return session.get('tipo_usuario') != 'professor' or not session.get('professor_id')


@professor_bp.route("/painel_professor")
def painel_professor():
    if _guard():
        return redirect('/login')

    professor = ProfessorDAO.buscar_por_id(session['professor_id'])
    if not professor:
        session.clear()
        return redirect('/logout')

    return render_template("painel_professor.html", professor=professor, alunos=professor.alunos_vinculados)


@professor_bp.route("/professor/aluno/<int:aluno_id>")
def detalhes_aluno_professor(aluno_id):
    if _guard():
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_id(aluno_id)
    if not aluno or aluno.professor_id != session['professor_id']:
        abort(403)

    avaliacoes = AvaliacaoDAO.listar_por_aluno(aluno.id)
    return render_template("dt_aluno_professor.html", u=aluno, avaliacoes=avaliacoes)


@professor_bp.route("/professor/aluno/<int:aluno_id>/avaliacoes", methods=["POST"])
def cadastrar_avaliacao(aluno_id):
    if _guard():
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_id(aluno_id)
    if not aluno or aluno.professor_id != session['professor_id']:
        abort(403)

    def campo_float(nome):
        valor = request.form.get(nome)
        return float(valor) if valor else None

    data_avaliacao = request.form.get('data')

    nova_avaliacao = Avaliacao(
        aluno_id=aluno.id,
        professor_id=session['professor_id'],
        data=date.fromisoformat(data_avaliacao) if data_avaliacao else date.today(),
        peso=campo_float('peso'),
        altura=campo_float('altura'),
        percentual_gordura=campo_float('percentual_gordura'),
        medida_peito=campo_float('medida_peito'),
        medida_cintura=campo_float('medida_cintura'),
        medida_quadril=campo_float('medida_quadril'),
        medida_braco=campo_float('medida_braco'),
        medida_coxa=campo_float('medida_coxa'),
        objetivo=(request.form.get('objetivo') or '').strip() or None,
        observacoes=(request.form.get('observacoes') or '').strip() or None,
    )

    AvaliacaoDAO.salvar(nova_avaliacao)
    flash('Avaliação registrada com sucesso.', 'sucesso')

    return redirect(f'/professor/aluno/{aluno.id}')


@professor_bp.route("/professor/avaliacoes/<int:avaliacao_id>/remover", methods=["POST"])
def remover_avaliacao(avaliacao_id):
    if _guard():
        return redirect('/login')

    avaliacao = AvaliacaoDAO.buscar_por_id(avaliacao_id)
    if not avaliacao or not avaliacao.aluno or avaliacao.aluno.professor_id != session['professor_id']:
        abort(403)

    aluno_id = avaliacao.aluno_id
    AvaliacaoDAO.remover(avaliacao_id)
    flash('Avaliação removida.', 'sucesso')

    return redirect(f'/professor/aluno/{aluno_id}')
