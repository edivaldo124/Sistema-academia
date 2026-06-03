from config import db


class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    mensalidade = db.Column(db.String(50), default='Em Dia')  # Situação/Status
    senha = db.Column(db.String(255), nullable=False)

    # Chave estrangeira para o plano
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id'), nullable=True)

    # Mapeamento do relacionamento para buscar os dados do plano automaticamente
    plano = db.relationship('Plano', backref='alunos', lazy=True)

    # Construtor da classe
    def __init__(self, nome, cpf, email, telefone, senha, mensalidade='Em Dia', plano_id=None):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.mensalidade = mensalidade
        self.plano_id = plano_id