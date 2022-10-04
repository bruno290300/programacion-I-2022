from flask import Blueprint, render_template, make_response
import requests
import json


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    return render_template('vista_principal.html')


@app.route('/login')
def login():
    api_url = "http://127.0.0.1:5000/auth/login"
    data = {"email": "rosales@gmail.com", "contraseña": "6666"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, json=data, headers=headers)
    print(response.status_code)
    print(response.text)

    token = json.loads(response.text)
    token = token["access_token"]
    print(token)

    resp = make_response(render_template("login.html"))
    resp.set_cookie("acess_token",token)

    return resp

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/mi-perfil')
def mi_perfil():
    return render_template('mi_perfil.html')

@app.route('/lista-poemas')
def lista_poemas():
    return render_template('lista_poemas.html')

