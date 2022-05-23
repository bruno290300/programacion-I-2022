from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decoradores import admin_required, admin_required_or_poeta_required



class Usuario(Resource):
    @jwt_required()
    def get(self, id):
        usuarios = db.session.query(UsuarioModel).get_or_404(id)
        return usuarios.to_json()

    @admin_required
    def delete(self, id):
        usuarios = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuarios)
        db.session.commit()
        return '', 204

    @jwt_required()
    def put(self, id):
        usuarios = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuarios, key, value)
        db.session.add(usuarios)
        db.session.commit()
        return usuarios.to_json() , 201



class Usuarios(Resource):
    @admin_required
    def get(self):

        page = 1

        per_page = 10

        usuarios = db.session.query(UsuarioModel)


        if request.get_json():
            filters = request.get_json().items()

            for key, value in filters:

                if key =="page":
                    page = int(value)

                if key == "per_page":
                    per_page = int(value)


                if key == "nombre":
                    usuarios = usuarios.filter(UsuarioModel.nombre.like('%'+value+'%'))
                
                
                
                # Order
                if key == "sort_by":

                    if value == 'nombre':
                        usuarios = usuarios.order_by(UsuarioModel.nombre)

                    if value == "num_poemas[desc]":
                        usuarios=usuarios.outerjoin(UsuarioModel.poemas).group_by(UsuarioModel.id).order_by(func.count(UsuarioModel.id).desc())
                    
                    if value == "num_poemas":
                        usuarios=usuarios.outerjoin(UsuarioModel.poemas).group_by(UsuarioModel.id).order_by(func.count(UsuarioModel.id))
                    
                    if value == "num_calificaciones":
                        usuarios=usuarios.outerjoin(UsuarioModel.calificaciones).group_by(UsuarioModel.id).order_by(func.count(UsuarioModel.id).desc())
        
        
        usuarios = usuarios.paginate(page, per_page, False, 30)
        return jsonify({
            'poemas' : [usuarios.to_json_short() for usuarios in usuarios.items],
            'total' : usuarios.total,
            'pages' : usuarios.pages,
            'page' : page
        })

    @admin_required
    def post(self):
        usuarios = UsuarioModel.from_json(request.get_json())
        db.session.add(usuarios)
        db.session.commit()
        return usuarios.to_json(), 201