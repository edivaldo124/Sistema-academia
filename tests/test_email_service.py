import smtplib
import unittest
from unittest.mock import patch

from flask import Flask

from servicos.email_service import enviar_email


class EmailServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            MAIL_SERVER='smtp.gmail.com',
            MAIL_PORT=587,
            MAIL_USE_TLS=True,
            MAIL_USERNAME='academia@gmail.com',
            MAIL_PASSWORD='abcd efgh ijkl mnop',
            MAIL_DEFAULT_SENDER='academia@gmail.com',
            MAIL_SENDER_NAME='Academia',
            MAIL_TIMEOUT=10,
        )

    @patch('servicos.email_service.smtplib.SMTP')
    def test_envia_email_com_tls_e_autenticacao(self, smtp_mock):
        conexao = smtp_mock.return_value.__enter__.return_value

        with self.app.app_context():
            resultado = enviar_email(
                'aluno@example.com',
                'Confirmação',
                'Cadastro realizado.'
            )

        self.assertTrue(resultado)
        smtp_mock.assert_called_once_with('smtp.gmail.com', 587, timeout=10)
        conexao.starttls.assert_called_once()
        conexao.login.assert_called_once_with('academia@gmail.com', 'abcdefghijklmnop')
        conexao.send_message.assert_called_once()

        mensagem = conexao.send_message.call_args.args[0]
        self.assertEqual(mensagem['To'], 'aluno@example.com')
        self.assertEqual(mensagem['Subject'], 'Confirmação')
        self.assertIn('Cadastro realizado.', mensagem.get_content())

    @patch('servicos.email_service.smtplib.SMTP')
    def test_nao_abre_conexao_sem_configuracao(self, smtp_mock):
        self.app.config.update(
            MAIL_USERNAME='',
            MAIL_PASSWORD='',
            MAIL_DEFAULT_SENDER='',
        )

        with self.app.app_context():
            resultado = enviar_email('aluno@example.com', 'Teste', 'Mensagem')

        self.assertFalse(resultado)
        smtp_mock.assert_not_called()

    @patch('servicos.email_service.smtplib.SMTP')
    def test_falha_de_autenticacao_nao_interrompe_aplicacao(self, smtp_mock):
        conexao = smtp_mock.return_value.__enter__.return_value
        conexao.login.side_effect = smtplib.SMTPAuthenticationError(535, b'erro')

        with self.assertLogs(level='ERROR'):
            with self.app.app_context():
                resultado = enviar_email('aluno@example.com', 'Teste', 'Mensagem')

        self.assertFalse(resultado)


if __name__ == '__main__':
    unittest.main()
