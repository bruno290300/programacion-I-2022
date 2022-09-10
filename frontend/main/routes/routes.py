from flask import Blueprint, render_template

app = Blueprint('app', __name__, url_prefix='/')


@app.route('/')
def index():
    return render_template('vista_principal.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/mi-perfil')
def mi_perfil():
    return render_template('mi_perfil.html')

@app.route('/lista-poemas')
def lista_poemas():
    return render_template('lista_poemas.html')

