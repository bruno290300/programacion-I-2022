from flask_restful import Resource
from flask import request


USUARIOS = {
    1: {'firstname': 'Pedro', 'lastname': 'Marco'},
    2: {'firstname': 'Leandro', 'lastname': 'Sosa'},
}


class Usuario(Resource):
    def get(self, id):
        if int(id) in USUARIOS:
            return USUARIOS[int(id)]
        return '', 404


    def delete(self, id):
        if int(id) in USUARIOS:
            del USUARIOS[int(id)]
            return '', 204
        return '', 404


    def put(self, id):
        if int(id) in USUARIOS:
            usuario = USUARIOS[int(id)]
            data = request.get_json()
            usuario.update(data)
            return usuario, 201
        return '', 404


class Usuarios(Resource):
    #Obtener lista de recursos
    def get(self):
        return USUARIOS
    #Insertar recurso
    def post(self):
        #Obtener datos de la solicitud
        usuario = request.get_json()
        id = int(max(USUARIOS.keys())) + 1
        USUARIOS[id] = usuario
        return USUARIOS[id], 201
