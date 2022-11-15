from flask import Flask, Blueprint, current_app, render_template, make_response, request, redirect, url_for
import requests
import json


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    api_url = "http://127.0.0.1:5000/poemas"
    data = { "page": 1, "per_page": 4 }
    headers = { "Content-Type": "application/json", "Authorization": f'Bearer {request.cookies.get("jwt")}' }
    response = requests.get(api_url, json=data, headers=headers)
    poemas = json.loads(response.text)
    print(poemas)
    return render_template('vista_principal.html', poemas=poemas['poemas'])




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

        lista = json.loads(response.text)
        
        token = lista["access_token"]
        
        id = lista["id"]
        print(id)
        resp = make_response(redirect(url_for('app.index')))

        resp.set_cookie("jwt",token)
        resp.set_cookie("id",id)

        return resp

    else:
        return render_template('login.html')


    

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/mi-perfil')
def mi_perfil():
    id = request.cookies.get("id")
    api_url = f"http://127.0.0.1:5000/usuario/{id}"
    headers = { "Content-Type": "application/json", "Authorization": f'Bearer {request.cookies.get("jwt")}' }
    response = requests.get(api_url, headers=headers)
    usuario = json.loads(response.text)
    print(usuario)



    return render_template('mi_perfil.html', usuario=usuario)

@app.route('/lista-poemas')
def lista_poemas():
    return render_template('lista_poemas.html')

