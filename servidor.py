from flask import *

# 1. IMPORTAR o db único do arquivo de configuração
from config import db

from blueprints.usuario_bp import auth_bp
from blueprints.adm_bp import admin_bp

app = Flask(__name__)
app.secret_key = "chave_secreta_academia"

# 2. DEFININDO A CONEXÃO COM O BANCO (Passo 5.1 do professor)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///academia_orm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. VINCULAR o servidor flask ao sqlalchemy (Resolve o seu erro!)
db.init_app(app)

# Registrando os blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# 4. CRIANDO CONTEXTO para gerar as tabelas automaticamente (Passo 5.2 do professor)
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


if __name__ == '__main__':
    app.run(debug=True)