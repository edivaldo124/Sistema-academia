import unittest

from sqlalchemy.engine import make_url

from config import opcoes_engine, preparar_url_banco


class TestConfiguracaoBanco(unittest.TestCase):
    def test_normaliza_url_do_supabase_e_exige_ssl(self):
        resultado = preparar_url_banco(
            "postgresql://postgres.ref:senha@aws-0-regiao.pooler.supabase.com:5432/postgres"
        )
        url = make_url(resultado)

        self.assertEqual(url.drivername, "postgresql+psycopg2")
        self.assertEqual(url.query["sslmode"], "require")

    def test_preserva_ssl_configurado(self):
        resultado = preparar_url_banco(
            "postgresql://usuario:senha@db.projeto.supabase.co/postgres?sslmode=verify-full"
        )

        self.assertEqual(make_url(resultado).query["sslmode"], "verify-full")

    def test_sqlite_nao_recebe_opcoes_de_pool(self):
        self.assertEqual(opcoes_engine("sqlite:///:memory:"), {})

    def test_url_vazia_e_rejeitada(self):
        with self.assertRaises(RuntimeError):
            preparar_url_banco("")


if __name__ == "__main__":
    unittest.main()
