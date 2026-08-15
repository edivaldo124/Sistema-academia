import click
from flask import Flask, render_template, session

from config import Config, db

from blueprints.usuario_bp import auth_bp
from blueprints.adm_bp import admin_bp
from servicos.email_service import enviar_email

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template('index.html')


@app.cli.command('testar-email')
@click.argument('destinatario')
def testar_email(destinatario):
    """Envia uma mensagem de teste sem criar uma rota pública."""
    enviado = enviar_email(
        destinatario,
        'Teste de e-mail da academia',
        'O Gmail SMTP foi configurado corretamente no sistema da academia.'
    )

    if not enviado:
        raise click.ClickException(
            'Não foi possível enviar. Confira as variáveis MAIL_* e o log do servidor.'
        )

    click.echo('E-mail de teste enviado com sucesso.')
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
