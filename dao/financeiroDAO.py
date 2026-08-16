from datetime import date

from config import db
from modelos.pagamento import Pagamento


class PagamentoDAO:
    @staticmethod
    def salvar(pagamento):
        db.session.add(pagamento)
        db.session.commit()

    @staticmethod
    def listar_por_aluno(aluno_id):
        pagamentos = Pagamento.query.filter_by(aluno_id=aluno_id).all()

        for p in pagamentos:
            if p.status == 'pendente' and p.vencimento < date.today():
                p.status = 'atrasado'

        db.session.commit()
        return pagamentos

    @staticmethod
    def buscar_por_id(pagamento_id):
        return Pagamento.query.filter_by(id=pagamento_id).first()

    @staticmethod
    def atualizar_status(pagamento_id, status, forma_pagamento):
        pagamento = Pagamento.query.filter_by(id=pagamento_id).first()

        if pagamento:
            pagamento.status = status
            pagamento.forma_pagamento = forma_pagamento

            if status == 'pago':
                pagamento.data_pagamento = date.today()
            else:
                pagamento.data_pagamento = None

            db.session.commit()
            return True

        return False
