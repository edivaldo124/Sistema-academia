import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


load_dotenv()


def ler_booleano(nome, padrao=False):
    valor = os.environ.get(nome)
    if valor is None:
        return padrao
    return valor.strip().lower() in {'1', 'true', 'sim', 'yes', 'on'}


class Config:
    SECRET_KEY_CONFIGURADA = bool(os.environ.get('SECRET_KEY', '').strip())
    SECRET_KEY = os.environ.get('SECRET_KEY', '').strip() or 'chave_secreta_academia'
    APP_BASE_URL = os.environ.get('APP_BASE_URL', '').strip().rstrip('/')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql+psycopg2://edivaldo:senha123@localhost/academia3_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = ler_booleano('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '').strip()
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '').strip()
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', '').strip() or MAIL_USERNAME
    MAIL_SENDER_NAME = os.environ.get('MAIL_SENDER_NAME', 'Academia').strip()
    MAIL_TIMEOUT = int(os.environ.get('MAIL_TIMEOUT', '10'))

    RESET_TOKEN_MAX_AGE = int(os.environ.get('RESET_TOKEN_MAX_AGE', '1800'))


db = SQLAlchemy()
