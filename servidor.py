from flask import Flask, render_template

from blueprints.usuario_bp import auth_bp
from blueprints.adm_bp import admin_bp

app = Flask(__name__)

app.secret_key = "chave_secreta_academia"

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

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

