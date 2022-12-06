from flask import Flask, Response, flash, redirect, render_template,request,jsonify, send_file, url_for
from flask_cors import CORS
from fpdf import FPDF
from database import db
from encriptador import bcrypt
from flask_migrate import Migrate
from config import BaseConfig
from models import User
from routes.user.user import appuser
from routes.images.images import imageUser
from flask_login import LoginManager,login_user,logout_user,login_required
from sqlalchemy import exc
from datetime import date,datetime
app = Flask(__name__)

# RUTAS BLUEPRINT
app.register_blueprint(appuser)
app.register_blueprint(imageUser)
app.config.from_object(BaseConfig)

CORS(app)

bcrypt.init_app(app)
db.init_app(app)

#MIGRACIONES
migrate = Migrate()
migrate.init_app(app, db)

#ERROR 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404/404.html"),404

#REDIRECCION HACIA LOGIN
@app.route('/')
def index():
    return redirect(url_for('login'))

#LOGIN
@app.route("/login",methods=['GET','POST'])
def login():
    # if request.method=='POST':
    #     pass
    #     # print(request.form['email'])
    #     # print(request.form['password'])
    #     # email = request.form['email']
    #     # password = request.form['password']
    #     # #aqui deberia validar si esta logeado como admin o usuario
    #     # #simulemos que esta como admin
    #     # if (email == 'jav@gmail.com' and password == '1234'):
    #     #    return redirect(url_for('home'))
        
    #     # else:
    #     #     flash("Usuario Incorrecto")
    #     #     return render_template('auth/login.html')
      
        
    # else:
        return render_template("auth/login.html")

#INICIOS
@app.route("/loginpublico")
def loginpublico():
    return render_template("home/homepublico.html")

@app.route("/home")
def home():
    return render_template("home/home.html")

#rutas para los registros y vistas
#USUARIOS
@app.route("/registro")
def registro():
    return render_template("usuarios/registrousuarios.html")

@app.route("/verusuarios")
def verusuarios():
    return render_template("usuarios/usuarios.html")

#VENTAS
@app.route("/verventas")
def verventas():
    return render_template("ventas/ventas.html")

@app.route("/registroventas")
def registroventas():
    return render_template("ventas/registroventas.html")

#ZAPATOS
@app.route("/verzapatos")
def verzapatos():
    return render_template("zapatos/zapatos.html")
@app.route("/registrozapatos")
def registrozapatos():
    return render_template("zapatos/registrozapatos.html")

#INVENTARIO
@app.route("/registroinventario")
def registroinventario():
    return render_template("inventario/registroinventario.html")

@app.route("/verinventario")
def verinventario():
    return render_template("inventario/inventario.html")

#CERRAR SESION
@app.route("/logout")
def logout():
    return render_template("logout/logout.html")

#SUBIR IMAGEN
@app.route("/imagen")
def imagen():
    return render_template("imagen/imagen.html")

#DESCARGAR PDF
@app.route('/descargarPdf')
def descargarPdf():
    usuarios = User.query.all()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(False)
    page_width = pdf.w - 2 * pdf.l_margin
            
    pdf.set_font('Times','B',14.0)
    pdf.cell(page_width,0.0,'Informacion de los Usuarios',align = 'C')
    pdf.ln(10)
            
    pdf.set_font('Arial',size=12)
    
    col_width = page_width/4
            
    pdf.ln(1)
            
    th = pdf.font_size
    pdf.cell(10,th,str('id'),border=1)
    pdf.cell(80,th,str('Email'),border=1)
    pdf.cell(80,th,str('Fecha De Creacion'),border=1)
    pdf.cell(20,th,str('Admin'),border=1)
    pdf.ln(th)  
    for usuario in usuarios:
        pdf.cell(10,th,str(usuario.id),border=1)
        pdf.cell(80,th,str(usuario.email),border=1)
        pdf.cell(80,th,str(format(usuario.registered_on)),border=1)
        pdf.cell(20,th,str(usuario.admin),border=1)
        pdf.ln(th)
        
    pdf.ln(10)
    pdf.image(
    "zapato.jpg", 80, 100, 50, 0, "", "https://pyfpdf.github.io/fpdf2/"
)    
    pdf.set_font('Times','',10.0)
    pdf.cell(page_width,0.0,'- Fin del Reporte -',align='C')
        
    return Response(pdf.output(dest='S'),mimetype='application/pdf',headers={'Content-Disposition':'attachment;filename=usuarios_report.pdf'})
            

           
if __name__ == '__main__':
    app.run(debug=True,port=5000)