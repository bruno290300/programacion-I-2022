from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel
#from flask_jwt_extended import jwt_required, get_jwt_identity
#from main.auth.decoradores import admin_required



'''
USUARIOS = {
    1: {'firstnombre': 'Pedro', 'lastnombre': 'Marco'},
    2: {'firstnombre': 'Leandro', 'lastnombre': 'Sosa'},
}
'''


class Usuario(Resource):
    #@jwt_required()
    def get(self, id):
        usuarios = db.session.query(UsuarioModel).get_or_404(id)
        return usuarios.to_json()

    #@admin_required
    def delete(self, id):
        usuarios = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuarios)
        db.session.commit()
        return '', 204

    #@jwt_required()
    def put(self, id):
        usuarios = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuarios, key, value)
        db.session.add(usuarios)
        db.session.commit()
        return usuarios.to_json() , 201



class Usuarios(Resource):
    #@jwt_required()
    def get(self):

        page = 1

        per_page = 10

        usuarios = db.session.query(UsuarioModel)


        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == "nombre":
                    usuarios = usuarios.filter(UsuarioModel.nombre.like('%'+value+'%'))
                if key == "email":
                    email = email.filter(UsuarioModel.email.like("%"+ value +"%"))
                
                
                # Order
                if key == "sort_by":
                    if value == 'nombre':
                        usuarios = usuarios.order_by(UsuarioModel.nombre)
                    if value == "nombre[des]":
                        nombre = nombre.order_by(UsuarioModel.nombre.desc())
                    if value == "email":
                        email = email.order_by(UsuarioModel.email)
                    if value == "email[desc]":
                        email = email.order_by(UsuarioModel.email.desc())   
        
        
        usuarios = usuarios.paginate(page, per_page, False, 30)
        return jsonify({
            'poemas' : [usuarios.to_json_short() for usuarios in usuarios.items],
            'total' : usuarios.total,
            'pages' : usuarios.pages,
            'page' : page
        })


    def post(self):
        usuarios = UsuarioModel.from_json(request.get_json())
        db.session.add(usuarios)
        db.session.commit()
        return usuarios.to_json(), 201