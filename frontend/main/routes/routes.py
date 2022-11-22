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
        if response.status_code == 200:
            lista = json.loads(response.text)
            
            token = lista["access_token"]
            
            id = lista["id"]
            print(id)
            resp = make_response(redirect(url_for('app.index')))

            resp.set_cookie("jwt",token)
            resp.set_cookie("id",id)

            return resp
        else:
            return render_template('login.html', error=response.text)
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

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie("jwt", "", expires=0)
    return resp

@app.route('/crear-poema', methods=['GET', 'POST'])
def crear_poema():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        cuerpo = request.form.get('cuerpo')
        api_url = "http://127.0.0.1:5000/poemas"
        id = request.cookies.get("id")
        data = {"titulo": titulo, "cuerpo": cuerpo, "usuarioId": id}
        jwt = request.cookies.get("jwt")
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {jwt}'}
        response = requests.post(api_url, json=data, headers=headers)
        if response.ok:
            return redirect(url_for('app.index'))
        else:
            return redirect(url_for('app.crear_poema'))

    return render_template('crear_poema.html')


@app.route('/editar-poema/<int:id>', methods=['GET', 'POST'])
def editar_poema(id):
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        cuerpo = request.form.get('cuerpo')
        api_url = f"http://127.0.0.1:5000/poema/{id}"
        id = request.cookies.get("id")
        data = {"titulo": titulo, "cuerpo": cuerpo}
        jwt = request.cookies.get("jwt")
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {jwt}'}
        response = requests.put(api_url, json=data, headers=headers)
        if response.ok:
            return redirect(url_for('app.index'))
        else:
            return redirect(url_for('app.index'))
        

    api_url = f"http://127.0.0.1:5000/poema/{id}"
    jwt = request.cookies.get("jwt")
    headers = {"Content-Type": "application/json", "Authorization": f'Bearer {jwt}'}
    response = requests.get(api_url, headers=headers)
    poema = json.loads(response.text)
    print(poema)
    return render_template('editar_poema.html', poema=poema)


@app.route('/eliminar-poema/<int:id>')
def eliminar_poema(id):
    api_url = "http://127.0.0.1:5000/poema/"+str(id)
    headers = { "Content-Type": "application/json", "Authorization": f'Bearer {request.cookies.get("jwt")}' }
    response = requests.delete(api_url, headers=headers)

    return make_response(redirect(url_for('app.index')))
    



    
    
       
