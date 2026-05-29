import sqlite3
from modelos.usuario import Usuario


class UsuarioDAO:
    def __init__(self, db_path="academia_v3.db"):  # Mudamos para v3 para criar a nova tabela automaticamente
        self.__db_path = db_path
        self._criar_tabelas()

    def _conectar(self):
        return sqlite3.connect(self.__db_path)

    def _criar_tabelas(self):
        conexao = self._conectar()
        cursor = conexao.cursor()

        # Tabela de usuários
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS usuarios
                       (
                           login TEXT PRIMARY KEY,
                           nome TEXT NOT NULL,
                           senha TEXT NOT NULL,
                           email TEXT NOT NULL,
                           telefone TEXT,
                           cpf TEXT,
                           plano TEXT DEFAULT 'Nenhum',
                           mensalidade TEXT DEFAULT 'Em Dia'
                       )
                       """)

        # NOVA TABELA: Tabela de planos cadastrados pelo Admin
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS planos
                       (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           nome_plano TEXT NOT NULL UNIQUE,
                           preco TEXT NOT NULL
                       )
                       """)

        # Insere o admin padrão se não existir
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE login = 'admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                           INSERT INTO usuarios (nome, login, senha, email, telefone, cpf, plano, mensalidade)
                           VALUES ('Administrador', 'admin', 'admin123', 'admin@academia.com', '00000000',
                                   '00000000000', 'Admin', 'Em Dia')
                           """)

        conexao.commit()
        conexao.close()

    # --- MÉTODOS DE PLANOS ---
    def cadastrar_plano(self, nome_plano, preco):
        try:
            conexao = self._conectar()
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO planos (nome_plano, preco) VALUES (?, ?)", (nome_plano, preco))
            conexao.commit()
            conexao.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def listar_planos(self):
        conexao = self._conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome_plano, preco FROM planos")
        linhas = cursor.fetchall()
        conexao.close()
        return linhas  # Retorna uma lista de tuplas [( 'Musculação', '80.00' ), ...]

    def remover_plano(self, nome_plano):
        """Método adicionado para remover o plano pelo nome_plano"""
        conexao = self._conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM planos WHERE nome_plano = ?", (nome_plano,))
        conexao.commit()
        conexao.close()

    # --- MÉTODOS DE USUÁRIOS ---
    def salvar(self, novo_usuario):
        try:
            conexao = self._conectar()
            cursor = conexao.cursor()
            cursor.execute("""
                           INSERT INTO usuarios (nome, login, senha, email, telefone, cpf, plano, mensalidade)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                           """, (novo_usuario.nome, novo_usuario.login, novo_usuario.senha,
                                 novo_usuario.email, novo_usuario.telefone, novo_usuario.cpf, novo_usuario.plano,
                                 novo_usuario.mensalidade))
            conexao.commit()
            conexao.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def remover(self, login):
        conexao = self._conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM usuarios WHERE login = ? AND login != 'admin'", (login,))
        conexao.commit()
        conexao.close()

    def atualizar_plano(self, login, novo_plano):
        conexao = self._conectar()
        cursor = conexao.cursor()
        cursor.execute("UPDATE usuarios SET plano = ? WHERE login = ?", (novo_plano, login))
        conexao.commit()
        conexao.close()

    def alterar_status_mensalidade(self, login, novo_status):
        conexao = self._conectar()
        cursor = conexao.cursor()
        cursor.execute("UPDATE usuarios SET mensalidade = ? WHERE login = ?", (novo_status, login))
        conexao.commit()
        conexao.close()

    def buscar_por_login(self, login):
        conexao = self._conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT nome, login, senha, email, telefone, cpf, plano, mensalidade FROM usuarios WHERE login = ?",
            (login,))
        r = cursor.fetchone()
        conexao.close()
        if r:
            return Usuario(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7])
        return None

    def autenticar(self, login, senha):
        conexao = self._conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT nome, login, senha, email, telefone, cpf, plano, mensalidade FROM usuarios WHERE login = ? AND senha = ?",
            (login, senha))
        r = cursor.fetchone()
        conexao.close()
        if r:
            return Usuario(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7])
        return None

    def listar_todos(self):
        conexao = self._conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT nome, login, senha, email, telefone, cpf, plano, mensalidade FROM usuarios WHERE login != 'admin'")
        linhas = cursor.fetchall()
        conexao.close()
        return [Usuario(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7]) for l in linhas]


dao_usuario = UsuarioDAO()