from .. import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return '<Usuario: %r %r %r %r>' % (self.nombre, self.email, self.contraseña, self.rol)

    #Convertir objeto en JSON
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'email': str(self.email),
            'contraseña': str(self.contraseña),
            'rol': str(self.rol),

        }
        return usuario_json

    def to_json_short(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre)

        }
        return usuario_json
    @staticmethod

    def from_json(usuario_json):
        id = usuario_json.get('id')
        nombre = usuario_json.get('nombre')
        email = usuario_json.get('email')
        contraseña = usuario_json.get('contraseña')
        rol = usuario_json.get('rol')
        return Usuario(id=id,
                    nombre=nombre,
                    email=email,
                    contraseña=contraseña,
                    rol=rol,
                    )
