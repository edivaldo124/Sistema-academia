import unittest

from flask import Flask

from config import db
from dao.usuarioDAO import AlunoDAO
from modelos.plano import Plano  # noqa: F401 - registra a tabela relacionada
from modelos.usuario import Aluno
from servicos.recuperacao_senha import buscar_aluno_pelo_token, gerar_token_recuperacao


class RecuperacaoSenhaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            SECRET_KEY='segredo-exclusivo-dos-testes',
            SQLALCHEMY_DATABASE_URI='sqlite://',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            RESET_TOKEN_MAX_AGE=1800,
        )
        db.init_app(self.app)
        self.contexto = self.app.app_context()
        self.contexto.push()
        db.create_all()

        self.aluno = Aluno(
            nome='Aluno Teste',
            login='aluno',
            datanascimento='2000-01-01',
            cpf='000.000.000-00',
            email='aluno@example.com',
            telefone='(00) 00000-0000',
            senha='senha-segura',
            descricao='',
        )
        db.session.add(self.aluno)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.contexto.pop()

    def test_token_valido_localiza_aluno(self):
        token = gerar_token_recuperacao(self.aluno)

        aluno_encontrado = buscar_aluno_pelo_token(token)

        self.assertEqual(aluno_encontrado.id, self.aluno.id)

    def test_token_adulterado_e_rejeitado(self):
        token = gerar_token_recuperacao(self.aluno)

        self.assertIsNone(buscar_aluno_pelo_token(token + 'alterado'))

    def test_token_deixa_de_valer_apos_alterar_senha(self):
        token = gerar_token_recuperacao(self.aluno)
        self.aluno.definir_senha('outra-senha-segura')
        db.session.commit()

        self.assertIsNone(buscar_aluno_pelo_token(token))

    def test_login_antigo_e_migrado_para_hash(self):
        self.aluno.senha = 'senha-antiga'
        db.session.commit()

        autenticado = AlunoDAO.autenticar('aluno', 'senha-antiga')

        self.assertEqual(autenticado.id, self.aluno.id)
        self.assertTrue(autenticado.senha_esta_protegida())
        self.assertNotEqual(autenticado.senha, 'senha-antiga')


if __name__ == '__main__':
    unittest.main()
