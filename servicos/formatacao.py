import re


def somente_digitos(valor):
    return re.sub(r'\D', '', valor or '')


def formatar_cpf(valor):
    digitos = somente_digitos(valor)[:11]
    if len(digitos) != 11:
        return (valor or '').strip()
    return f'{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}'


def variantes_cpf(valor):
    digitos = somente_digitos(valor)
    if len(digitos) != 11:
        return [(valor or '').strip()]
    return [digitos, formatar_cpf(digitos)]


def formatar_telefone(valor):
    digitos = somente_digitos(valor)[:11]
    if len(digitos) == 11:
        return f'({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}'
    if len(digitos) == 10:
        return f'({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}'
    return (valor or '').strip()
