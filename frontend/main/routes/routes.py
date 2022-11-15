from flask import Flask, Blueprint, current_app, render_template, make_response, request, redirect, url_for
import requests
import json


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    api_url = "http://127.0.0.1:5000/poemas"
    data = { "page": 1, "per_page": 10 }
    headers = { "Content-Type": "application/json", "Authorization": f'Bearer {request.cookies.get("jwt")}' }
    response = requests.get(api_url, json=data, headers=headers)
    print(response.status_code)  
    print(response.text)
    poemas = json.loads(response.text)
    print(poemas)
    return render_template('vista_principal.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('correo')
        password = request.form.get('contraseña')
        print(email)
        print(password)
        api_url = "http://127.0.0.1:5000/auth/login"
        data = {"email": email, "contraseña": password}
        headers = {"Content-Type": "application/json"}
        response = requests.post(api_url, json=data, headers=headers)
        print(response.status_code)
        print(response.text)

        token = json.loads(response.text)
        token = token["access_token"]
        print(token)
        resp = make_response(render_template("vista_principal.html"))

        resp.set_cookie("jwt",token)

        return resp

    else:
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

