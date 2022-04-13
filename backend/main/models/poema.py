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
            'fecha_hora': self.fecha_hora.strftime('%Y-%m-%d')

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
        fecha_hora = datetime.strptime(poema_json.get('fecha_hora'), '%Y-%m-%d')
        return Poema(id=id,
                    usuarioId=usuarioId,
                    titulo=titulo,
                    cuerpo=cuerpo,
                    fecha_hora=fecha_hora
                    )



