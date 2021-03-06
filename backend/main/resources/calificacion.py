from xmlrpc.client import TRANSPORT_ERROR
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CalificacionModel, UsuarioModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decoradores import admin_required, admin_required_or_poeta_required, poeta_required
from flask_mail import Mail
from main.mail.functions import sendMail



class Calificacion(Resource):
    @jwt_required()
    def get(self, id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        return calificacion.to_json()

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        id_usuario = get_jwt_identity()
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        if "rol" in claims:    
            if claims["rol"] == "admin" or id_usuario == calificacion.usuarioId:
                db.session.delete(calificacion)
                db.session.commit()
                return '', 204
            else:
                return "Este usuario no está autorizado para realizar esta acción."
        

    @jwt_required()
    def put(self, id):
        id_usuario = get_jwt_identity()
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        if id_usuario == calificacion.usuarioId:
            data = request.get_json().items()
            for key, value in data:
                setattr(calificacion, key, value)
            
            db.session.add(calificacion)
            db.session.commit() 
            return calificacion.to_json(), 201   
        else:
            return "Este usuario no está autorizado para realizar esta acción."


class Calificaciones(Resource):
    @jwt_required(optional=True)
    def get(self):
        claims = get_jwt()
        if "rol" in claims:
            if claims["rol"] == "admin":
                calificaciones = db.session.query(CalificacionModel)
                return jsonify([calificacion.to_json() for calificacion in calificaciones])
            else:
                calificaciones = db.session.query(CalificacionModel)
                return jsonify([calificacion.to_json() for calificacion in calificaciones])    
        

    @jwt_required()
    def post(self):
        id_usuario = get_jwt_identity()
        calificacion = CalificacionModel.from_json(request.get_json())
        usuario_calificacion = db.session.query(UsuarioModel).get(id_usuario)
        claims = get_jwt()

        if "rol" in claims:
            if claims['rol'] == "poeta":
                
                calificacion.usuarioId = int(id_usuario)
                db.session.add(calificacion)
                db.session.commit()
                sent = sendMail([calificacion.poema.usuario.email],"Has recibido una calificación",'register',usuario_calificacion = usuario_calificacion, 
                usuario = calificacion.poema.usuario, poema=calificacion.poema)

                return calificacion.to_json(), 201
            else:
                return "Este usuario no está autorizado para realizar esta acción."

