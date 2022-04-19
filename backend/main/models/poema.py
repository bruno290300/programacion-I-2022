from .. import db
from datetime import datetime
from sqlalchemy.sql import func


class Poema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuarioId = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    cuerpo = db.Column(db.String(100), nullable=False)
    fecha_hora = db.Column(db.DateTime(timezone=True), default=func.now())

    usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship("Usuario", back_populates="poema", cascade="all, delete-orphan")
    calificacion = db.relationship("Calificacion", back_populates="poema", cascade="all, delete-orphan")

    def __repr__(self):
        return '<Poema: %r %r %r %r>' % (self.usuarioId, self.titulo, self.cuerpo, self.fecha_hora)


    def to_json(self):
        self.usuario = db.session.query(UsuarioModel).get_or_404(self.usuarioId)
        self.calificacion = db.session.query(CalificacionModel).get_or_404(self.calificacionId)
        poema_json = {
            'id': self.id,
            'usuarioId': str(self.usuarioId),
            'titulo': str(self.titulo),
            'cuerpo': str(self.cuerpo),
            'usuario': self.usuario.to_json(),
            'calificacion': self.calificacion.to_json()


        }
        return poema_json



    def to_json_short(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'cuerpo': str(self.cuerpo)


        }
        return poema_json


    @staticmethod

    def from_json(poema_json):
        id = poema_json.get('id')
        usuarioId = poema_json.get('usuarioId')
        titulo = poema_json.get('titulo')
        cuerpo = poema_json.get('cuerpo')

        return Poema(id=id,
                    usuarioId=usuarioId,
                    titulo=titulo,
                    cuerpo=cuerpo
                    )



