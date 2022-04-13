from .. import db

class Calificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuarioId = db.Column(db.Integer, nullable=False)
    poemaId = db.Column(db.Integer, nullable=False)
    puntaje = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return '< Poema: %r %r >' % (self.puntaje, self.comentario)
    
    
    
    def to_json(self):
        calificacion_json = {
            'id': self.id,
            'puntaje': str(self.puntaje),
            'comentario': str(self.comentario)
            
        }
        return calificacion_json

    def to_json_short(self):
        calificacion_json = {
            'id': self.id,
            'puntaje': str(self.puntaje),
            'comentario': str(self.comentario)

        }
        return calificacion_json
    @staticmethod
    

    def from_json(calificacion_json):
        id = calificacion_json.get('id')
        usuarioId = calificacion_json.get('usuarioId')
        poemaId = calificacion_json.get('poemaId')
        puntaje = calificacion_json.get('puntaje')
        comentario = calificacion_json.get('comentario')
        return Calificacion(id=id,
                    usuarioid=usuarioId,
                    poemaid=poemaId,
                    puntaje=puntaje,
                    comentario=comentario
                    )