from flask import *
from config import db
import os

from blueprints.usuario_bp import auth_bp
from blueprints.adm_bp import admin_bp

app = Flask(__name__)
app.secret_key = "chave_secreta_academia"

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
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)