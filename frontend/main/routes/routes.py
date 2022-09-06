from flask import Blueprint, render_template

app = Blueprint('app', __name__, url_prefix='/')


@app.route('/')
def index():
    return render_template('vista_principal.html')


@app.route('/login')
def login():
    return render_template('login.html')