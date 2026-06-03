import sqlite3

class FinanceiroDAO:
    def __init__(self, db_path="academia_v3.db"):
        self.__db_path = db_path
        self._criar_tabela()

    def _conectar(self):
        return sqlite3.connect(self.__db_path, timeout=10)

    def _criar_tabela(self):
        conexao = self._conectar()
        try:
            cursor = conexao.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS faturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                data_vencimento TEXT NOT NULL,
                valor REAL NOT NULL,
                status_pagamento TEXT DEFAULT 'Pendente',
                forma_pagamento TEXT,
                FOREIGN KEY (aluno_id) REFERENCES alunos(id)
            )
            """)
            conexao.commit()
        finally:
            conexao.close()

    def gerar_fatura(self, aluno_id, data_vencimento, valor):
        conexao = self._conectar()
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO faturas (aluno_id, data_vencimento, valor, status_pagamento)
                VALUES (?, ?, ?, 'Pendente')
            """, (aluno_id, data_vencimento, valor))
            conexao.commit()
        finally:
            conexao.close()

    def registrar_pagamento(self, fatura_id, forma_pagamento):
        conexao = self._conectar()
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE faturas 
                SET status_pagamento = 'Pago', forma_pagamento = ? 
                WHERE id = ?
            """, (forma_pagamento, fatura_id))
            conexao.commit()
        finally:
            conexao.close()

dao_financeiro = FinanceiroDAO()