from flask import Blueprint, Response, request,jsonify
from sqlalchemy import exc
from models import User,Zapato,Venta
from app import db,bcrypt
from auth import tokenCheck
from fpdf import FPDF 
appuser = Blueprint('appsuer',__name__,template_folder="templates")

#USUARIO
@appuser.route('/auth/registro', methods =['POST'])
def registro():
    user  = request.get_json()
    userExists = User.query.filter_by(email=user['email']).first()
    if not userExists:
        usuario = User(email=user["email"],password=user["password"])
        try:
            db.session.add(usuario)
            db.session.commit()
            mensaje="Usuario creado"
        except exc.SQLAlchemyError as e:
            mensaje = "Error"
    else:
        mensaje="Usuario existente"     
    return jsonify({"message":mensaje})

@appuser.route('/auth/login' , methods =['POST'])
def login():
    user  = request.get_json()
    usuario = User(email=user["email"],password=user["password"])
    searchUser = User.query.filter_by(email = usuario.email).first()
    if searchUser:
        validation = bcrypt.check_password_hash(searchUser.password,user["password"])
        if validation:
            auth_token = usuario.encode_auth_token(user_id=searchUser.id)
            responseObject = {
                    'status': 'success',
                    'message': 'Loggin exitoso',
                    'auth_token': auth_token
                }
            return jsonify(responseObject)
    return jsonify({"message":"Datos incorrectos"})

@appuser.route('/usuarios', methods=['GET'])
@tokenCheck
def getUsers(usuario):

    if usuario['admin']:
        output = []
        usuarios = User.query.all()
        for usuario in usuarios:
            usuarioData = {}
            usuarioData['id'] = usuario.id
            usuarioData['email'] = usuario.email
            usuarioData['password'] = usuario.password
            usuarioData['registered_on'] = usuario.registered_on
            usuarioData['admin'] = usuario.admin
            output.append(usuarioData)
        return jsonify({'usuarios':output})



#ZAPATOS
#registro zapato
@appuser.route('/auth/registrozapato', methods =['POST'])
def registrozapato():
    zapato  = request.get_json()
    print(zapato)
    producto = Zapato(nombre=zapato["nombre"],modelo=zapato["modelo"],precio=zapato["precio"],talla=zapato["talla"])
    try:
        db.session.add(producto)
        db.session.commit()
        mensaje="Producto creado"
    except exc.SQLAlchemyError as e:
            mensaje = "Error"
      
    return jsonify({"message":mensaje})

#mostrar Zapatos
@appuser.route('/zapatos', methods=['GET'])
@tokenCheck
def getZapatos(zapato):
        output = []
        zapatos = Zapato.query.all()
        for zapato in zapatos : 
            zapatoData = {}
            zapatoData['id'] = zapato.id
            zapatoData['nombre'] = zapato.nombre
            zapatoData['modelo'] = zapato.modelo
            zapatoData['precio'] = zapato.precio
            zapatoData['talla'] = zapato.talla
            output.append(zapatoData)
        return jsonify({'zapatos':output})

#Eliminar Zapato
@appuser.route('/auth/eliminarzapato/<int:ID>', methods =['DELETE'])
def eliminarzapato(ID):
    zapato_to_delete = Zapato.query.get_or_404(ID)
    try:
        db.session.delete(zapato_to_delete)
        db.session.commit()
        mensaje="Zapato eliminado"
    except exc.SQLAlchemyError as e:
        mensaje = "Error"
    return jsonify({"message":mensaje})

#ACTUALIZAR ZAPATO
@appuser.route('/auth/actualizarzapato/<int:ID>', methods =['PUT'])
def actualizarzapato(ID):
    zapato  = request.get_json()
    print("-----")
    print(zapato)
    zapato_to_update = Zapato.query.get_or_404(ID)
    zapato_to_update.nombre =zapato['nombre']
    zapato_to_update.modelo =zapato['modelo']
    zapato_to_update.precio =zapato['precio']
    zapato_to_update.talla =zapato['talla']
    try:
        db.session.commit()
        mensaje="Zapato actualizado"
    except exc.SQLAlchemyError as e:
        mensaje = "Error"
    return jsonify({"message":mensaje})


@appuser.route('/zapatos/<int:ID>', methods=['GET'])
def get_zapato(ID):
    output = []
    zapato = Zapato.query.get_or_404(ID)
    zapatoData = {}
    zapatoData['id'] = zapato.id
    zapatoData['nombre'] = zapato.nombre
    zapatoData['modelo'] = zapato.modelo
    zapatoData['precio'] = zapato.precio
    zapatoData['talla'] = zapato.talla
    output.append(zapatoData)
    
    return jsonify({'zapatos':output})

#Ventas
#registro venta
@appuser.route('/auth/registroventa', methods =['POST'])
def registroventa():
    venta  = request.get_json()
    print(venta)
    ticket = Venta(referencia=venta["referencia"],cantidad=venta["cantidad"])
    try:
        db.session.add(ticket)
        db.session.commit()
        mensaje="ticket creado"
    except exc.SQLAlchemyError as e:
            mensaje = "Error"
      
    return jsonify({"message":mensaje})

#mostrar ventas
@appuser.route('/ventas', methods=['GET'])
@tokenCheck
def getVentas(venta):
        output = []
        ventas = Venta.query.all()
        for venta in ventas : 
            ventaData  = {}
            ventaData['id'] = venta.id
            ventaData['referencia'] = venta.referencia
            ventaData['cantidad'] = venta.cantidad
            
            output.append(ventaData)
        return jsonify({'ventas':output})

#Eliminar venta
@appuser.route('/auth/eliminarventa/<int:ID>', methods =['DELETE'])
def eliminarventa(ID):
    venta_to_delete = Venta.query.get_or_404(ID)
    try:
        db.session.delete(venta_to_delete)
        db.session.commit()
        mensaje="venta eliminado"
    except exc.SQLAlchemyError as e:
        mensaje = "Error"
    return jsonify({"message":mensaje})

#ACTUALIZAR venta
@appuser.route('/auth/actualizarventa/<int:ID>', methods =['PUT'])
def actualizarventa(ID):
    venta  = request.get_json()
    print("-----venta")
    print(venta)
    print("-----venta")
    venta_to_update = Venta.query.get_or_404(ID)
    venta_to_update.referencia =venta['referencia']
    venta_to_update.cantidad =venta['cantidad']

    try:
        db.session.commit()
        mensaje="venta actualizada"
    except exc.SQLAlchemyError as e:
        mensaje = "Error"
    return jsonify({"message":mensaje})


@appuser.route('/ventas/<int:ID>', methods=['GET'])
def get_venta(ID):
    output = []
    venta = Venta.query.get_or_404(ID)
    ventaData = {}
    ventaData['id'] = venta.id
    ventaData['referencia'] = venta.referencia
    ventaData['cantidad'] = venta.cantidad

    output.append(ventaData)
    
    return jsonify({'ventas':output})






#ELIMINAR USUARIO
@appuser.route('/auth/eliminar/<int:ID>', methods =['DELETE'])
def eliminar(ID):
    user_to_delete = User.query.get_or_404(ID)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        mensaje="Usuario eliminado"
    except exc.SQLAlchemyError as e:
        mensaje = "Error"
    return jsonify({"message":mensaje})

#ACTUALIZAR USUARIO
@appuser.route('/auth/actualizar/<int:ID>', methods =['PUT'])
def actualizar(ID):
    usuario  = request.get_json()
    user_to_update = User.query.get_or_404(ID)
    user_to_update.email =usuario['email']
    user_to_update.password =usuario['password']
    try:
        db.session.commit()
        mensaje="Usuario actualizado"
    except exc.SQLAlchemyError as e:
        mensaje = "Error"
    return jsonify({"message":mensaje})


@appuser.route('/usuarios/<int:ID>', methods=['GET'])
def get_user(ID):
    output = []
    usuario = User.query.get_or_404(ID)
    usuarioData = {}
    usuarioData['id'] = usuario.id
    usuarioData['email'] = usuario.email
    usuarioData['password'] = usuario.password
    usuarioData['registered_on'] = usuario.registered_on
    usuarioData['admin'] = usuario.admin
    output.append(usuarioData)
    
    return jsonify({'usuarios':output})