from datetime import datetime
from email.policy import default
from sqlalchemy import column
from .. import db
from sqlalchemy import func
from statistics import mean




class Poema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuarioId = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    cuerpo = db.Column(db.String(100), nullable=False)
    fecha_hora = db.Column(db.DateTime(timezone=True), default=func.now())

    
    usuario = db.relationship('Usuario', back_populates="poemas",uselist=False,single_parent=True)
    calificaciones = db.relationship("Calificacion", back_populates="poema", cascade="all, delete-orphan")

    def __repr__(self):
        return '<Poema: %r %r %r %r>' % (self.usuarioId, self.titulo, self.cuerpo, self.fecha_hora)

    def promedio_puntaje(self):
        lista_calificacion = []
        
        if len(self.calificaciones) == 0:
            mean = 0
        else:
            for calificacion in self.calificaciones:
                puntaje = calificacion.puntaje
                lista_calificacion.append(puntaje)
            mean = statistics.mean(lista_calificacion)
            return mean


    def to_json(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'cuerpo': str(self.cuerpo),
            'usuario': self.usuario.to_json(),
            'fecha_hora': str(self.fecha_hora.strftime("%d-%m-%Y")),
            'calificaciones': [calificacion.to_json() for calificacion in self.calificaciones],
            'promedio_calificacion': self.promedio_puntaje()
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



