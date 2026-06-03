from config import db
from modelos.usuario import Aluno

class AlunoDAO:
    @staticmethod
    def salvar(aluno):
        db.session.add(aluno)
        db.session.commit()

    @staticmethod
    def listar_todos():
        return Aluno.query.all()

    @staticmethod
    def autenticar(usuario, senha):
        # Procura se o texto digitado coincide com nome, email OU cpf, E se a senha bate
        return Aluno.query.filter(
            ((Aluno.nome == usuario) | (Aluno.email == usuario) | (Aluno.cpf == usuario)) &
            (Aluno.senha == senha)
        ).first()

    @staticmethod
    def buscar_por_usuario(usuario):
        # Busca o perfil pelo nome, email ou cpf que está salvo na sessão
        return Aluno.query.filter(
            (Aluno.nome == usuario) | (Aluno.email == usuario) | (Aluno.cpf == usuario)
        ).first()

    @staticmethod
    def atualizar_mensalidade(cpf, nova_situacao):
        aluno = Aluno.query.filter_by(cpf=cpf).first()
        if aluno:
            aluno.mensalidade = nova_situacao
            db.session.commit()
            return True
        return False

    @staticmethod
    def remover(cpf):
        aluno = Aluno.query.filter_by(cpf=cpf).first()
        if aluno:
            db.session.delete(aluno)
            db.session.commit()
            return True
        return False