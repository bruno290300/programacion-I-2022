from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CalificacionModel



'''
CALIFICACIONES = {
    1: {'calificacion': '5',},
    2: {'calificacion': '6',},
}
'''


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
        calificaciones = db.session.query(CalificacionModel).all()
        return jsonify([calificacion.to_json() for calificacion in calificaciones])



    def post(self):
        calificacion = CalificacionModel.from_json(request.get_json())
        db.session.add(calificacion)
        db.session.commit()
        return calificacion.to_json(), 201
