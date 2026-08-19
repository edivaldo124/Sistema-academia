import unittest
from unittest.mock import patch, MagicMock
from servidor import app
from config import db
from modelos.usuario import Aluno
from dao.usuarioDAO import AlunoDAO

class TestAlteracaoCredenciais(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            aluno = Aluno(
                nome="Carlos Silva",
                login="carlos",
                datanascimento="1990-01-01",
                cpf="111.222.333-44",
                email="carlos@teste.com",
                telefone="(11) 98888-7777",
                senha="senha_antiga",
                descricao="Nenhuma"
            )
            db.session.add(aluno)
            db.session.commit()
            self.aluno_id = aluno.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_editar_perfil_requer_login(self):
        response = self.app.get('/perfil/editar')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    @patch('blueprints.usuario_bp.enviar_codigo_verificacao')
    def test_fluxo_completo_alteracao_credenciais(self, mock_enviar_email):
        mock_enviar_email.return_value = (True, "E-mail enviado")

        # 1. Simula login
        with self.app.session_transaction() as sess:
            sess['usuario'] = 'carlos'
            sess['aluno_id'] = self.aluno_id
            sess['tipo_usuario'] = 'aluno'

        # 2. Acessa tela de edição
        response = self.app.get('/perfil/editar')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Editar credenciais', response.data)

        # 3. Submete novas credenciais (novo nome, novo login, nova senha)
        response_post = self.app.post('/perfil/editar', data={
            'nome': 'Carlos Silva Atualizado',
            'login': 'carlos_novo',
            'datanascimento': '1990-01-01',
            'email': 'carlos.novo@teste.com',
            'telefone': '(11) 99999-8888',
            'descricao': 'Sem restrições',
            'senha_atual': 'senha_antiga',
            'nova_senha': 'senha_nova_123',
            'confirmar_senha': 'senha_nova_123'
        }, follow_redirects=False)

        # Deve redirecionar para tela de verificação de código
        self.assertEqual(response_post.status_code, 302)
        self.assertIn('/perfil/verificar_codigo', response_post.headers['Location'])
        self.assertTrue(mock_enviar_email.called)

        # 4. Recupera código gerado na sessão
        with self.app.session_transaction() as sess:
            codigo = sess['pendente_alteracao']['codigo']
            self.assertEqual(len(codigo), 6)

        # 5. Testa código incorreto
        resp_erro = self.app.post('/perfil/verificar_codigo', data={'codigo': '000000'})
        self.assertEqual(resp_erro.status_code, 200)
        self.assertIn(b'incorreto', resp_erro.data)

        # 6. Submete código correto
        resp_sucesso = self.app.post('/perfil/verificar_codigo', data={'codigo': codigo}, follow_redirects=True)
        self.assertEqual(resp_sucesso.status_code, 200)

        # 7. Verifica se dados foram atualizados no banco
        with app.app_context():
            aluno_atualizado = db.session.get(Aluno, self.aluno_id)
            self.assertEqual(aluno_atualizado.nome, 'Carlos Silva Atualizado')
            self.assertEqual(aluno_atualizado.login, 'carlos_novo')
            self.assertEqual(aluno_atualizado.email, 'carlos.novo@teste.com')
            self.assertEqual(aluno_atualizado.senha, 'senha_nova_123')


class TestEmailServico(unittest.TestCase):
    @patch('servicos.email_servico.requests.post')
    def test_enviar_email_brevo(self, mock_post):
        from servicos.email_servico import _enviar_email_brevo
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        sucesso, msg = _enviar_email_brevo(
            destinatario="aluno@teste.com",
            assunto="Teste",
            conteudo_texto="Texto",
            conteudo_html="<p>Texto</p>",
            api_key="chave_teste",
            remetente="remetente@teste.com"
        )
        self.assertTrue(sucesso)
        self.assertEqual(msg, "E-mail enviado com sucesso.")
        self.assertTrue(mock_post.called)

    @patch('servicos.email_servico.requests.post')
    def test_enviar_email_resend(self, mock_post):
        from servicos.email_servico import _enviar_email_resend
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        sucesso, msg = _enviar_email_resend(
            destinatario="aluno@teste.com",
            assunto="Teste",
            conteudo_texto="Texto",
            conteudo_html="<p>Texto</p>",
            api_key="chave_teste",
            remetente="remetente@teste.com"
        )
        self.assertTrue(sucesso)
        self.assertEqual(msg, "E-mail enviado com sucesso.")
        self.assertTrue(mock_post.called)


if __name__ == '__main__':
    unittest.main()

