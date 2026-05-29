class Usuario:
    def __init__(self, nome, login, senha, email, telefone, cpf, plano="Nenhum", mensalidade="Em Dia"):
        # Atributos privados usando dois underlines (__)
        self.__nome = nome
        self.__login = login
        self.__senha = senha
        self.__email = email
        self.__telefone = telefone
        self.__cpf = cpf
        self.__plano = plano
        self.__mensalidade = mensalidade

    # --- NOME ---
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    # --- LOGIN ---
    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, login):
        self.__login = login

    # --- SENHA ---
    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, senha):
        self.__senha = senha

    # --- EMAIL ---
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    # --- TELEFONE ---
    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
        self.__telefone = telefone

    # --- CPF ---
    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf

    # --- PLANO ---
    @property
    def plano(self):
        return self.__plano

    @plano.setter
    def plano(self, plano):
        self.__plano = plano

    # --- MENSALIDADE ---
    @property
    def mensalidade(self):
        return self.__mensalidade

    @mensalidade.setter
    def mensalidade(self, mensalidade):
        self.__mensalidade = mensalidade