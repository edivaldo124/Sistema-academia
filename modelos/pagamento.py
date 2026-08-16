from config import db


class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    __table_args__ = (
        db.CheckConstraint('valor > 0', name='ck_pagamentos_valor_positivo'),
        db.CheckConstraint(
            "status IN ('pendente', 'pago', 'atrasado', 'cancelado')",
            name='ck_pagamentos_status_valido'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False, index=True)
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id'), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    vencimento = db.Column(db.Date, nullable=False, index=True)
    data_pagamento = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pendente', index=True)
    forma_pagamento = db.Column(db.String(30), nullable=True)

    aluno = db.relationship('Aluno', backref=db.backref('pagamentos', lazy=True))
    plano = db.relationship('Plano', backref=db.backref('pagamentos', lazy=True))

    def atualizar_atraso(self, hoje):
        if self.status == 'pendente' and self.vencimento < hoje:
            self.status = 'atrasado'
