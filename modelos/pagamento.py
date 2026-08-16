from config import db


class Pagamento(db.Model):
    __tablename__ = 'pagamentos'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pendente')
    forma_pagamento = db.Column(db.String(30), nullable=True)

    aluno = db.relationship('Aluno', backref='pagamentos', lazy=True)
    plano = db.relationship('Plano', backref='pagamentos', lazy=True)

    def __init__(self, aluno_id, plano_id, valor, vencimento, status='pendente', data_pagamento=None, forma_pagamento=None):
        self.aluno_id = aluno_id
        self.plano_id = plano_id
        self.valor = valor
        self.vencimento = vencimento
        self.status = status
        self.data_pagamento = data_pagamento
        self.forma_pagamento = forma_pagamento
