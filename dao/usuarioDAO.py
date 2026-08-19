from config import db
from modelos.plano import Plano
from modelos.usuario import Aluno
from datetime import date, timedelta
from sqlalchemy.exc import SQLAlchemyError
from servicos.formatacao import variantes_cpf

class AlunoDAO:
    @staticmethod
    def salvar(aluno):
        db.session.add(aluno)
        db.session.commit()

    @staticmethod
    def listar_todos():
        return Aluno.query.all()

    @staticmethod
    def buscar_por_id(aluno_id):
        return db.session.get(Aluno, aluno_id)

    @staticmethod
    def autenticar(usuario, senha):
        # Agora exigimos obrigatoriamente que a senha bata com o usuário, email, login ou cpf.
        cpfs_possiveis = variantes_cpf(usuario)
        return Aluno.query.filter(
            (
                    (Aluno.nome == usuario) |
                    (Aluno.login == usuario) |
                    (Aluno.email == usuario) |
                    (Aluno.cpf.in_(cpfs_possiveis))
                    
            ) & (Aluno.senha == senha)
        ).first()

    @staticmethod
    def buscar_por_usuario(usuario):
        # Busca o perfil pelo nome, email ou cpf que está salvo na sessão
        return Aluno.query.filter(
            (Aluno.nome == usuario) |(Aluno.login == usuario)| (Aluno.email == usuario) | (Aluno.descricao == usuario)| (Aluno.cpf == usuario)
        ).first()

    @staticmethod
    def login_em_uso_por_outro(login, aluno_id):
        return Aluno.query.filter(Aluno.login == login, Aluno.id != aluno_id).first() is not None

    @staticmethod
    def email_em_uso_por_outro(email, aluno_id):
        return Aluno.query.filter(Aluno.email == email, Aluno.id != aluno_id).first() is not None

    @staticmethod
    def atualizar_mensalidade(cpf, nova_situacao):
        aluno = Aluno.query.filter_by(cpf=cpf).first()
        if aluno:
            aluno.mensalidade = nova_situacao
            db.session.commit()
            return True
        return False

    @staticmethod
    def remover(aluno_id):
        aluno = db.session.get(Aluno, aluno_id)
        if not aluno:
            return None

        try:
            db.session.delete(aluno)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @staticmethod
    def atualizar_credenciais_aluno(aluno_id, dados):
        aluno = db.session.get(Aluno, aluno_id)
        if not aluno:
            return False

        try:
            if 'nome' in dados and dados['nome']:
                aluno.nome = dados['nome'].strip()
            if 'login' in dados and dados['login']:
                aluno.login = dados['login'].strip()
            if 'email' in dados and dados['email']:
                aluno.email = dados['email'].strip().lower()
            if 'telefone' in dados:
                aluno.telefone = dados['telefone']
            if 'datanascimento' in dados and dados['datanascimento']:
                aluno.datanascimento = dados['datanascimento'].strip()
            if 'descricao' in dados:
                aluno.descricao = (dados.get('descricao') or '').strip()
            if dados.get('nova_senha'):
                aluno.senha = dados['nova_senha']

            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @staticmethod
    def atualizar_dados_completos(cpf, dados):
        aluno = Aluno.query.filter_by(cpf=cpf).first()
        if aluno:
            aluno.nome = dados.get('nome')
            aluno.login = dados.get('login')
            aluno.datanascimento = dados.get('datanascimento')
            aluno.email = dados.get('email')

            # Garantir que não enviam None para campos de texto opcionais
            aluno.telefone = dados.get('telefone', '')
            aluno.mensalidade = dados.get('mensalidade', 'Pendente')
            aluno.descricao = dados.get('descricao', '')

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
