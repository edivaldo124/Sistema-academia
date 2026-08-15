import hashlib

from flask import current_app
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from modelos.usuario import Aluno


SALT_RECUPERACAO = 'recuperacao-de-senha'


def _assinatura_senha(aluno):
    return hashlib.sha256(aluno.senha.encode('utf-8')).hexdigest()[:16]


def gerar_token_recuperacao(aluno):
    serializador = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    dados = {
        'aluno_id': aluno.id,
        'assinatura_senha': _assinatura_senha(aluno),
    }
    return serializador.dumps(dados, salt=SALT_RECUPERACAO)


def buscar_aluno_pelo_token(token):
    serializador = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    tempo_maximo = current_app.config.get('RESET_TOKEN_MAX_AGE', 1800)

    try:
        dados = serializador.loads(
            token,
            salt=SALT_RECUPERACAO,
            max_age=tempo_maximo,
        )
    except (BadSignature, SignatureExpired):
        return None

    aluno = Aluno.query.filter_by(id=dados.get('aluno_id')).first()
    if not aluno:
        return None

    if dados.get('assinatura_senha') != _assinatura_senha(aluno):
        return None

    return aluno
