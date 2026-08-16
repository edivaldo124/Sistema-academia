from flask import *
from config import db
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

from blueprints.usuario_bp import auth_bp
from blueprints.adm_bp import admin_bp

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave_secreta_academia-desenvolvimento')

# Mantem a sessao no cookie, mas limita seu tempo de vida e impede acesso via JS.
app.config.update(
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=os.environ.get('COOKIE_SECURE', 'false').lower() == 'true',
    SESSION_REFRESH_EACH_REQUEST=True,
)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql+psycopg2://edivaldo:senha123@localhost/academia3_db'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def pagina_login():
    return render_template("login.html")

@app.route("/cadastrar")
def pagina_cadastro():
    return render_template("cadastro.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
