from config import db
from modelos.professor import Professor
from sqlalchemy.exc import SQLAlchemyError
from servicos.formatacao import variantes_cpf


class ProfessorDAO:
    @staticmethod
    def salvar(professor):
        db.session.add(professor)
        db.session.commit()

    @staticmethod
    def listar_todos():
        return Professor.query.all()

    @staticmethod
    def buscar_por_id(professor_id):
        return db.session.get(Professor, professor_id)

    @staticmethod
    def autenticar(usuario, senha):
        cpfs_possiveis = variantes_cpf(usuario)
        return Professor.query.filter(
            (
                    (Professor.nome == usuario) |
                    (Professor.login == usuario) |
                    (Professor.email == usuario) |
                    (Professor.cpf.in_(cpfs_possiveis))
            ) & (Professor.senha == senha)
        ).first()

    @staticmethod
    def remover(professor_id):
        professor = db.session.get(Professor, professor_id)
        if not professor:
            return None

        try:
            db.session.delete(professor)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
