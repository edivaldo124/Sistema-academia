from config import db
from modelos.plano import Plano
from modelos.usuario import Aluno
from datetime import date, timedelta

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
            ((Aluno.nome == usuario) |(Aluno.login == usuario)|(Aluno.datanascimento == usuario)| (Aluno.email == usuario) | (Aluno.cpf == usuario)) &
            (Aluno.senha == senha)
        ).first()

    @staticmethod
    def buscar_por_usuario(usuario):
        # Busca o perfil pelo nome, email ou cpf que está salvo na sessão
        return Aluno.query.filter(
            (Aluno.nome == usuario) |(Aluno.login == usuario)| (Aluno.email == usuario) | (Aluno.cpf == usuario)
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




    @staticmethod
    def atualizar_dados_completos(cpf, dados):
        aluno = Aluno.query.filter_by(cpf=cpf).first()
        if aluno:
            aluno.nome = dados.get('nome')
            aluno.login = dados.get('login')
            aluno.datanascimento = dados.get('datanascimento')
            aluno.email = dados.get('email')
            aluno.telefone = dados.get('telefone')
            aluno.mensalidade = dados.get('mensalidade')

            plano_escolhido = dados.get('plano_id')

            # SE O ADMIN ESCOLHEU UM PLANO NOVO:
            if plano_escolhido and plano_escolhido != 'Nenhum':
                plano_id_int = int(plano_escolhido)

                # Só calcula o vencimento novo se o plano for diferente do que ele já tinha
                if aluno.plano_id != plano_id_int:
                    aluno.plano_id = plano_id_int

                    # 1. Puxa os dados do plano escolhido
                    plano_banco = Plano.query.get(plano_id_int)

                    # 2. Pega a data de hoje e soma com a duração do plano
                    hoje = date.today()
                    data_vencimento = hoje + timedelta(days=plano_banco.duracao_dias)

                    # 3. Guarda a data final no formato YYYY-MM-DD
                    aluno.data_vencimento = data_vencimento.strftime('%Y-%m-%d')
            else:
                aluno.plano_id = None
                aluno.data_vencimento = None  # Sem plano, sem vencimento

            db.session.commit()
            return True
        return False