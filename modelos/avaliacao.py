from config import db


class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    peso = db.Column(db.Float, nullable=True)
    altura = db.Column(db.Float, nullable=True)
    percentual_gordura = db.Column(db.Float, nullable=True)
    medida_peito = db.Column(db.Float, nullable=True)
    medida_cintura = db.Column(db.Float, nullable=True)
    medida_quadril = db.Column(db.Float, nullable=True)
    medida_braco = db.Column(db.Float, nullable=True)
    medida_coxa = db.Column(db.Float, nullable=True)
    objetivo = db.Column(db.String(255), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    aluno = db.relationship('Aluno', backref='avaliacoes', lazy=True)
    professor = db.relationship('Professor', backref='avaliacoes', lazy=True)

    def __init__(self, aluno_id, professor_id, data, peso=None, altura=None, percentual_gordura=None,
                 medida_peito=None, medida_cintura=None, medida_quadril=None, medida_braco=None,
                 medida_coxa=None, objetivo=None, observacoes=None):
        self.aluno_id = aluno_id
        self.professor_id = professor_id
        self.data = data
        self.peso = peso
        self.altura = altura
        self.percentual_gordura = percentual_gordura
        self.medida_peito = medida_peito
        self.medida_cintura = medida_cintura
        self.medida_quadril = medida_quadril
        self.medida_braco = medida_braco
        self.medida_coxa = medida_coxa
        self.objetivo = objetivo
        self.observacoes = observacoes

    @property
    def imc(self):
        if not self.peso or not self.altura:
            return None
        return round(self.peso / (self.altura ** 2), 2)
