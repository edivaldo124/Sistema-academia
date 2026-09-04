from config import db


class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    senha = db.Column(db.String(255), nullable=False)
    especialidade = db.Column(db.String(150), nullable=True)
    cref = db.Column(db.String(20), nullable=True)

    def __init__(self, nome, login, cpf, email, telefone, senha, especialidade=None, cref=None):
        self.nome = nome
        self.login = login
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.especialidade = especialidade
        self.cref = cref
