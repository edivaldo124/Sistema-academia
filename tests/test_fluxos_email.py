import unittest
from pathlib import Path
from unittest.mock import patch

from flask import Flask

from blueprints.adm_bp import admin_bp
from blueprints.usuario_bp import auth_bp
from config import db
from modelos.plano import Plano  # noqa: F401 - registra a tabela relacionada
from modelos.usuario import Aluno
from servicos.recuperacao_senha import buscar_aluno_pelo_token, gerar_token_recuperacao


PASTA_PROJETO = Path(__file__).resolve().parents[1]


class FluxosEmailTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(
            __name__,
            template_folder=str(PASTA_PROJETO / 'templates'),
        )
        self.app.config.update(
            TESTING=True,
            SECRET_KEY='segredo-exclusivo-dos-testes',
            SECRET_KEY_CONFIGURADA=True,
            SQLALCHEMY_DATABASE_URI='sqlite://',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            MAIL_SERVER='smtp.gmail.com',
            MAIL_PORT=587,
            MAIL_USE_TLS=True,
            MAIL_USERNAME='academia@gmail.com',
            MAIL_PASSWORD='senha-de-aplicativo',
            MAIL_DEFAULT_SENDER='academia@gmail.com',
            MAIL_SENDER_NAME='Academia',
            MAIL_TIMEOUT=10,
            RESET_TOKEN_MAX_AGE=1800,
        )
        db.init_app(self.app)
        self.app.register_blueprint(auth_bp)
        self.app.register_blueprint(admin_bp)
        self.contexto = self.app.app_context()
        self.contexto.push()
        db.create_all()
        self.cliente = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.contexto.pop()

    def criar_aluno(self):
        aluno = Aluno(
            nome='Aluno Teste',
            login='aluno',
            datanascimento='2000-01-01',
            cpf='000.000.000-00',
            email='aluno@example.com',
            telefone='(00) 00000-0000',
            senha='senha-segura',
            descricao='',
        )
        db.session.add(aluno)
        db.session.commit()
        return aluno

    def autenticar_admin(self):
        with self.cliente.session_transaction() as sessao:
            sessao['usuario'] = 'admin'

    @patch('blueprints.usuario_bp.enviar_boas_vindas', return_value=True)
    def test_cadastro_salva_hash_e_envia_boas_vindas(self, enviar_boas_vindas):
        resposta = self.cliente.post(
            '/cadastrar',
            data={
                'nomeusuario': 'Novo Aluno',
                'loginusuario': 'novo',
                'dataNascimento': '2001-02-03',
                'cpfusuario': '111.111.111-11',
                'senhausuario': 'senha-segura',
                'emailusuario': 'novo@example.com',
                'telefoneusuario': '(11) 11111-1111',
                'descricaousuario': '',
            },
            follow_redirects=True,
        )

        aluno = Aluno.query.filter_by(login='novo').first()
        self.assertEqual(resposta.status_code, 200)
        self.assertIsNotNone(aluno)
        self.assertTrue(aluno.senha_esta_protegida())
        enviar_boas_vindas.assert_called_once_with(aluno)

    @patch('blueprints.usuario_bp.enviar_link_recuperacao', return_value=True)
    def test_recuperacao_envia_link_sem_receber_nova_senha(self, enviar_link):
        aluno = self.criar_aluno()

        resposta = self.cliente.post(
            '/recuperar_senha',
            data={'cpf': aluno.cpf, 'email': aluno.email},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b'Se os dados estiverem corretos', resposta.data)
        enviar_link.assert_called_once()
        self.assertIn('/redefinir_senha/', enviar_link.call_args.args[1])

    @patch('blueprints.usuario_bp.enviar_senha_alterada', return_value=True)
    def test_link_nao_pode_ser_reutilizado_apos_troca(self, enviar_aviso):
        aluno = self.criar_aluno()
        token = gerar_token_recuperacao(aluno)

        resposta = self.cliente.post(
            f'/redefinir_senha/{token}',
            data={
                'nova_senha': 'outra-senha-segura',
                'confirmar_senha': 'outra-senha-segura',
            },
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertIsNone(buscar_aluno_pelo_token(token))
        enviar_aviso.assert_called_once_with(aluno)

    @patch('blueprints.usuario_bp.enviar_plano_selecionado', return_value=True)
    def test_selecao_de_plano_envia_confirmacao(self, enviar_plano):
        aluno = self.criar_aluno()
        plano = Plano(nome_plano='Mensal', preco_plano=80, duracao_dias=30)
        db.session.add(plano)
        db.session.commit()

        with self.cliente.session_transaction() as sessao:
            sessao['usuario'] = aluno.login

        resposta = self.cliente.post('/perfil', data={'plano': str(plano.id)})

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(aluno.plano_id, plano.id)
        enviar_plano.assert_called_once_with(aluno, plano)

    @patch('blueprints.adm_bp.enviar_status_mensalidade', return_value=True)
    def test_inativacao_envia_aviso_de_status(self, enviar_status):
        aluno = self.criar_aluno()

        self.autenticar_admin()

        resposta = self.cliente.get(f'/admin/remover/{aluno.cpf}')

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(aluno.mensalidade, 'Inativo')
        enviar_status.assert_called_once_with(aluno)

    def test_edicao_rejeita_email_que_ja_pertence_a_outro_aluno(self):
        aluno = self.criar_aluno()
        outro = Aluno(
            nome='Outro Aluno',
            login='outro',
            datanascimento='1999-01-01',
            cpf='111.111.111-11',
            email='outro@example.com',
            telefone='(11) 11111-1111',
            senha='senha-segura',
            descricao='',
        )
        db.session.add(outro)
        db.session.commit()
        self.autenticar_admin()

        resposta = self.cliente.post(
            f'/admin/usuario/{aluno.cpf}',
            data={
                'nome': aluno.nome,
                'login': aluno.login,
                'datanascimento': aluno.datanascimento,
                'email': outro.email,
                'telefone': aluno.telefone,
                'mensalidade': aluno.mensalidade,
                'plano_id': 'Nenhum',
                'descricao': aluno.descricao,
            },
            follow_redirects=True,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b'j\xc3\xa1 est\xc3\xa1 cadastrado para outro aluno', resposta.data)
        self.assertEqual(aluno.email, 'aluno@example.com')


if __name__ == '__main__':
    unittest.main()
