from config import db
from modelos.avaliacao import Avaliacao


class AvaliacaoDAO:
    @staticmethod
    def salvar(avaliacao):
        db.session.add(avaliacao)
        db.session.commit()

    @staticmethod
    def listar_por_aluno(aluno_id):
        return Avaliacao.query.filter_by(aluno_id=aluno_id).order_by(Avaliacao.data.desc()).all()

    @staticmethod
    def buscar_por_id(avaliacao_id):
        return db.session.get(Avaliacao, avaliacao_id)

    @staticmethod
    def remover(avaliacao_id):
        avaliacao = db.session.get(Avaliacao, avaliacao_id)
        if avaliacao:
            db.session.delete(avaliacao)
            db.session.commit()
            return True
        return False
