from .. import db

class Calificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    poemaId = db.Column(db.Integer, db.ForeignKey('poema.id'), nullable=False)
    puntaje = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(100), nullable=False)


    usuario = db.relationship('Usuario', back_populates="calificaciones",uselist=False,single_parent=True)
    poema = db.relationship('Poema', back_populates="calificaciones",uselist=False,single_parent=True)


    def __repr__(self):
        return '< Poema: %r %r >' % (self.puntaje, self.comentario, self.usuarioId, self.poemaId)
    

    def to_json(self):
        calificacion_json = {
            'id': self.id,
            'puntaje': str(self.puntaje),
            'comentario': str(self.comentario),
            'usuarioId': self.usuario.to_json(),
            'poemaId': self.poema.to_json_short()
            
        }
        return calificacion_json

    def to_json_complete(self):
        poema = poema.to_json()
        usuario = [usuarios.to_json() for usuarios in self.usuario]
        calificacion_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'contraseña': str(self.contraseña),
            'rol': str(self.rol),
            'email': str(self.email),
            'poema': poema,
            'usuario': usuario
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