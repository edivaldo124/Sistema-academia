from config import db


class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    datanascimento = db.Column(db.String, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    mensalidade = db.Column(db.String(50), default='pendente', nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)

    # Chave estrangeira para o plano
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id'), nullable=True)

    # Mapeamento do relacionamento para buscar os dados do plano automaticamente
    plano = db.relationship('Plano', backref='alunos', lazy=True)
    data_vencimento = db.Column(db.String(10), nullable=True)

    # Construtor da classe
    def __init__(self, nome, login,datanascimento, cpf, email, telefone, senha, descricao, mensalidade='pendente', plano_id=None, data_vencimento=None):
        self.nome = nome
        self.login = login
        self.datanascimento = datanascimento
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.descricao = descricao
        self.mensalidade = mensalidade
        self.plano_id = plano_id
        self.data_vencimento = data_vencimento