from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(100), nullable=False)

    poemas = db.relationship("Poema", back_populates="usuario",cascade="all, delete-orphan")
    calificaciones = db.relationship("Calificacion", back_populates="usuario", cascade="all, delete-orphan")

    @property
    def plain_password(self):
        raise AttributeError('Password cant be read')

    # Setter de la contraseña toma un valor en texto plano
    # calcula el hash y lo guarda en el atributo password
    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    # Método que compara una contraseña en texto plano con el hash guardado en la db
    def validate_pass(self, password):
        return check_password_hash(self.password, password)

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

    def to_json_complete(self):
        poemas = [poema.to_json() for poema in self.poemas]
        calificaciones = [calificacion.to_json() for calificacion in self.calificaciones]
        usuario_json = {
            'id': self.id,
            'name': str(self.name),
            'password': str(self.password),
            'rol': str(self.rol),
            'email': str(self.email),
            'poemas':poemas,
            'calificaciones':calificaciones
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
