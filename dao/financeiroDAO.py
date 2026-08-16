from datetime import date

from config import db
from modelos.pagamento import Pagamento


class PagamentoDAO:
    STATUS_VALIDOS = {'pendente', 'pago', 'atrasado', 'cancelado'}
    FORMAS_VALIDAS = {'pix', 'dinheiro', 'cartao_credito', 'cartao_debito', 'boleto'}

    @staticmethod
    def salvar(pagamento):
        db.session.add(pagamento)
        db.session.commit()
        return pagamento

    @staticmethod
    def listar_por_aluno(aluno_id):
        pagamentos = Pagamento.query.filter_by(aluno_id=aluno_id).order_by(
            Pagamento.vencimento.desc(), Pagamento.id.desc()
        ).all()

        houve_alteracao = False
        hoje = date.today()
        for pagamento in pagamentos:
            status_anterior = pagamento.status
            pagamento.atualizar_atraso(hoje)
            houve_alteracao = houve_alteracao or pagamento.status != status_anterior

        if houve_alteracao:
            db.session.commit()

        return pagamentos

    @staticmethod
    def buscar_por_id(pagamento_id):
        return db.session.get(Pagamento, pagamento_id)

    @staticmethod
    def atualizar_status(pagamento, status, forma_pagamento=None, data_pagamento=None):
        if status not in PagamentoDAO.STATUS_VALIDOS:
            return False

        pagamento.status = status
        if status == 'pago':
            pagamento.forma_pagamento = forma_pagamento
            pagamento.data_pagamento = data_pagamento or date.today()
        elif status in {'pendente', 'atrasado'}:
            pagamento.data_pagamento = None
            pagamento.forma_pagamento = None

        db.session.commit()
        return True
