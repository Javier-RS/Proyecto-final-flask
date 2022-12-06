
import jwt
import datetime
from config import BaseConfig
from app import db, bcrypt


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password,BaseConfig.BCRYPT_LOG_ROUNDS
        ).decode()
        
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                BaseConfig.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, BaseConfig.SECRET_KEY,algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError as e:
            print(e)
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError as e:
            print(e)
            return 'Invalid token. Please log in again.'


class Images(db.Model):
    __tablename__ = 'user_images' 

    id_imagen = db.Column(db.Integer,  primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False) #Actual data, needed for Download
    rendered_data = db.Column(db.Text, nullable=False)#Data to render the pic in browser
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # define relationship
    region = db.relationship('User', backref='users')

    def __repr__(self):
        return f'Pic ID: {self.id} Data: {self.data} text: {self.text} user: {self.user_id}'


class Empleado(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250))
    salario = db.Column(db.Integer)
    edad = db.Column(db.Integer)
    horas = db.Column(db.Integer)

    
    def __str__(self) -> str:
        return (f'ID : {self.id} ,'
                f'Nombre : {self.nombre} ,'
                f'Apellido: {self.apellido} ,'
                f'Email: {self.email},'  
                f'Salario: {self.salario},'
                f'Edad: {self.edad},'
                f'Horas: {self.horas}'      
                )
        
class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer,primary_key=True)
    referencia = db.Column(db.String(250))
    cantidad = db.Column(db.String(250))
    fecha = db.Column(db.DateTime)
    
    
    def __str__(self) -> str:
        return (f'ID : {self.id} ,'
                f'Referencia : {self.referencia} ,'
                f'Cantidad: {self.cantidad} ,'
                f'Fecha: {self.fecha},'
                   
                )
        


class Zapato(db.Model):
    __tablename__ = 'zapatos'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(250))
    modelo = db.Column(db.String(250))
    precio = db.Column(db.Integer)
    talla = db.Column(db.Integer)
    
    def __str__(self) -> str:
        return (f'ID : {self.id} ,'
                f'Nombre : {self.nombre} ,'
                f'Apellido: {self.apellido} ,'
                f'Email: {self.email}'
                    
                )


