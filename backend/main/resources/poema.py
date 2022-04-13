from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemaModel


'''
POEMAS = {
    1: {'titulo': 'La Rosa',},
    2: {'titulo': 'Martin Fierro',},
}
'''


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
        poemas = db.session.query(PoemaModel).all()
        return jsonify([poema.to_json_short() for poema in poemas])



    def post(self):
        poema = PoemaModel.from_json(request.get_json())
        db.session.add(Poema)
        db.session.commit()
        return poema.to_json(), 201
