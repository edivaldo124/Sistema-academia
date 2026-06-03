from config import db
from modelos.plano import Plano

class PlanoDAO:
    @staticmethod
    def salvar(plano):
        db.session.add(plano)
        db.session.commit()

    @staticmethod
    def listar_todos():
        return Plano.query.all()

    @staticmethod
    def buscar_por_id(id_plano):
        return Plano.query.filter_by(id=id_plano).first()

    @staticmethod
    def remover(id_plano):
        plano = Plano.query.filter_by(id=id_plano).first()
        if plano:
            db.session.delete(plano)
            db.session.commit()
            return True
        return False