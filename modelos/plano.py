from config import db

class Plano(db.Model):
    __tablename__ = 'planos'

    id = db.Column(db.Integer, primary_key=True)
    nome_plano = db.Column(db.String(100), nullable=False)
    preco_plano = db.Column(db.Float, nullable=False)

    duracao_dias = db.Column(db.Integer, nullable=False, default=30)

    def __init__(self, nome_plano, preco_plano, duracao_dias):
        self.nome_plano = nome_plano
        self.preco_plano = preco_plano
        self.duracao_dias = duracao_dias