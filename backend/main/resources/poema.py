from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemaModel
import datetime
from sqlalchemy import func




class Poema(Resource):
    def get(self, id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        return poema.to_json()

    def delete(self, id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        db.session.delete(poema)
        db.session.commit()
        return '', 204


'''
    def put(self, id):
        if int(id) in POEMAS:
            poema = POEMAS[int(id)]
            data = request.get_json()
            poema.update(data)
            return poema, 201
        return '', 404
'''

class Poemas(Resource):
    def get(self):
        #poemas = db.session.query(PoemaModel).all()
        #return jsonify([poema.to_json_short() for poema in poemas])

        page = 1

        per_page = 10

        poemas = db.session.query(PoemaModel)


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

                if key == "usuario":
                    poemas = poemas.filter(PoemaModel.usuario == value)
                #fecha
                if key == "created[gt]":
                    poemas = poemas.filter(PoemaModel.fecha_hora >= datetime.strptime(value, '%d-%m-%Y'))
                if key == "created[lt]":
                    poemas = poemas.filter(PoemaModel.fecha_hora <= datetime.strptime(value, '%d-%m-%Y'))
                
                
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
        
        
        poemas = poemas.paginate(page, per_page, False, 30)
        return jsonify({
            "poemas" : [poema.to_json_short() for poema in poemas.items],
            "total" : poemas.total,
            "pages" : poemas.pages,
            "page" : page
            })


    def post(self):
        poema = PoemaModel.from_json(request.get_json())
        db.session.add(poema)
        db.session.commit()
        return poema.to_json(), 201
