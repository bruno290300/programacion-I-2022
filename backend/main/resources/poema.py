from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemaModel, UsuarioModel, CalificacionModel
import datetime
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt



class Poema(Resource):
    @jwt_required()
    def get(self, id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        return poema.to_json()

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        id_usuario = get_jwt_identity()
        poema = db.session.query(PoemaModel).get_or_404(id)
        if "rol" in claims:
            if claims['rol'] == "admin" or id_usuario == int(poema.usuarioId):
                db.session.delete(poema)
                db.session.commit()
                return '', 204
            else:
                return "Este usuario no puede realizar esa acción"


    @jwt_required() #Requisito de admin o usuario para ejecutar esta función. Obligatorio Token
    def put(self, id):

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        poem = db.session.query(PoemaModel).get_or_404(id)

        #Verifico si el id del usuario concuerda con el que realiza la modificación o si es admin.
        if (claims['id'] == poem.usuarioId or claims['rol'] == "admin"):
            data = request.get_json().items()
            for key, value in data:
                setattr(poem, key, value)
            db.session.add(poem)
            db.session.commit()
            return poem.to_json(), 201
        else:
            return 'No tiene rol', 403


class Poemas(Resource):
    @jwt_required(optional=True)
    def get(self):

        poemas = db.session.query(PoemaModel)
        
        page = 1

        per_page = 10

        claims = get_jwt()

        identify_usuario = get_jwt_identity()

        # #if identify_usuario:
        #     #if request.get_json():
        #         #filters = request.get_json().items()
        #         #for key, value in filters:
        #             #if key =="page":
        #                 page = int(value)
        #             if key == "per_page":
        #                 per_page = int(value)
        #     poemas = db.session.query(PoemaModel).filter(PoemaModel.usuarioId != identify_usuario)
        #     poemas = poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by(func.count(PoemaModel.calificaciones))


        #else:
        if request.get_json():
            filters = request.get_json().items()

            for key, value in filters:
            
            # Paginate
            
                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
            
                if key == "titulo":
                    poemas = poemas.filter(PoemaModel.titulo.like('%'+value+'%'))

                if key == "usuarioId":
                    poemas = poemas.filter(PoemaModel.usuarioId == value)
            #fecha
                if key == "fecha_hora[gt]":
                    poemas = poemas.filter(PoemaModel.fecha_hora >= datetime.strptime(value, '%d-%m-%Y'))
                if key == "fecha_hora[lt]":
                    poemas = poemas.filter(PoemaModel.fecha_hora <= datetime.strptime(value, '%d-%m-%Y'))
            
                if key == 'username':
                    poemas = poemas.username(PoemaModel.usuario.has(UsuarioModel.username.like('%'+value+'%')))
            
            # Order
                if key == "sort_by":
                    if value == "usuario":
                        poemas = poemas.order_by(PoemaModel.usuario)
                    if value == "usuario[desc]":
                        poemas = poemas.order_by(PoemaModel.usuario.desc())
                    if value == "fecha_hora":
                        poemas == poemas.order_by(PoemaModel.fecha_hora)
                    if value == "fecha_hora[desc]":
                        poemas = poemas.order_by(PoemaModel.fecha_hora.desc())
                    if value == "calificaciones":
                        poemas = poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by(func.mean(PoemaModel.resultado))
                    if value == "calificaciones[desc]":
                        poemas = poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by(func.mean(PoemaModel.resultado).desc())
            
            

        
        poemas = poemas.paginate(page= page, per_page=per_page, error_out=False)
        return jsonify({
            "poemas" : [poema.to_json_short() for poema in poemas.items],
            "total" : poemas.total,
            "pages" : poemas.pages,
            "page" : page
            })
        
        
            

    @jwt_required()
    def post(self):
        id_usuario = get_jwt_identity()
        
        poema = PoemaModel.from_json(request.get_json())
        poema.usuarioId = id_usuario
        usuario = db.session.query(UsuarioModel).get_or_404(id_usuario)
        claims = get_jwt()

        if "rol" in claims:
            if claims["rol"] == "poeta" or claims["rol"] == "admin":
                poema.usuario_id = id_usuario
                db.session.add(poema)
                db.session.commit()
                return poema.to_json(), 201   
                    
            else:
                return "Este usuario no puede realizar esta acción."

    
    @jwt_required() #Requisito de admin o usuario para ejecutar esta función. Obligatorio Token
    def put(self, id):

        #Obtener claims de adentro del JWT
        claims = get_jwt()

        poem = db.session.query(PoemaModel).get_or_404(id)

        #Verifico si el id del usuario concuerda con el que realiza la modificación o si es admin.
        if (claims['id'] == poem.usuarioId or claims['rol'] == "admin"):
            data = request.get_json().items()
            for key, value in data:
                setattr(poem, key, value)
            db.session.add(poem)
            db.session.commit()
            return poem.to_json(), 201
        else:
            return 'No tiene rol', 403 #La solicitud no incluye información de autenticación
        
        


