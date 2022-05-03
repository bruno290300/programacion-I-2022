from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CalificacionModel




class Calificacion(Resource):
    def get(self, id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        return calificacion.to_json()


    def delete(self, id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        db.session.delete(calificacion)
        db.session.commit()
        

'''
    def put(self, id):
        if int(id) in CALIFICACIONES:
            calificacion = CALIFICACIONES[int(id)]
            data = request.get_json()
            calificacion.update(data)
            return calificacion, 201
        return '', 404
'''

class Calificaciones(Resource):
    def get(self):
        #calificaciones = db.session.query(CalificacionModel).all()
        #return jsonify([calificacion.to_json() for calificacion in calificaciones])
        page = 1
        per_page = 10
        calificaciones = db.session.query(CalificacionModel)


        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:

                #paginate
                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
                if key == "puntaje":
                    puntaje = puntaje.filter(CalificacionModel.puntaje == value)
                if key == "comentario":
                    comentario = comentario.filter(CalificacionModel.comentario.like("%" + value + "%"))
                if key == "usuario":
                    usuarioId = usuarioId.filter(CalificacionModel.usuarioId == value)
                if key == "poema":
                    poemaId = poemaId.filter(CalificacionModel.poemaId == value)
                
                #Order
                if key == "sort_by":
                    if value == "puntaje":
                        puntaje = puntaje.order_by(CalificacionModel.puntaje)
                    if value == "puntaje[desc]":
                        puntaje = puntaje.order_by(CalificacionModel.puntaje.desc())
                    if value == "usuario":
                        usuario = usuario.order_by(CalificacionModel.usuarioId)
                    if value == "usuario[des]":
                        usuario = usuario.order_by(CalificacionModel.usuarioId.desc())
                    if value == "poema":
                        poema = poema.order_by(CalificacionModel.poemaId)
                    if value == "poema[des]":
                        poema = poema.order_by(CalificacionModel.poemaId.desc())
                        
                
        calificaciones = calificaciones.paginate(page, per_page, False, 30)
        return jsonify({
            "poemas" : [calificaciones.to_json_short() for calificacion in calificaciones.items],
            "total" : calificaciones.total,
            "pages" : calificaciones.pages,
            "page" : page
            
            })        




    def post(self):
        calificacion = CalificacionModel.from_json(request.get_json())
        db.session.add(calificacion)
        db.session.commit()
        return calificacion.to_json(), 201
