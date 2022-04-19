from .. import db

class Calificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #usuarioId = db.Column(db.Integer, nullable=False)
    #poemaId = db.Column(db.Integer, nullable=False)
    puntaje = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(100), nullable=False)


    usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    poemaId = db.Column(db.Integer, db.ForeignKey('poema.id'), nullable=False)
    usuario = db.relationship("Usuario", back_populates="calificacion",cascade="all, delete-orphan")
    poema = db.relationship("Poema", back_populates="calificacion",cascade="all, delete-orphan")


    def __repr__(self):
        return '< Poema: %r %r >' % (self.puntaje, self.comentario)
    

    def to_json(self):
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.usuarioId)
        self.poema = db.session.query(PoemaModel).get_or_404(self.poemaId)
        calificacion_json = {
            'id': self.id,
            'puntaje': str(self.puntaje),
            'comentario': str(self.comentario),
            'usuario': self.usuario.to_json(),
            'poema': self.poema.to_json()
            
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
                    usuarioId=usuarioId,
                    poemaId=poemaId,
                    puntaje=puntaje,
                    comentario=comentario
                    )