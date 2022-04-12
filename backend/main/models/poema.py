from .. import db

class Poema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuarioId = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    cuerpo = db.Column(db.String(100), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Poema: %r %r %r %r>' % (self.usuarioId, self.titulo, self.cuerpo, self.fecha_hora)


    def to_json(self):
        poema_json = {
            'id': self.id,
            'usuarioId': str(self.usuarioId),
            'titulo': str(self.titulo),
            'cuerpo': str(self.cuerpo),
            'fecha_hora': self.fecha_hora,

        }
        return poema_json

