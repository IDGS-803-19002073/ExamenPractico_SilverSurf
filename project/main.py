#Importamos la clase Blueprint del módulo flask
from flask import Blueprint, render_template,flash
#Importamos login_required, current_user de flask_security
from flask_security import login_required, current_user
#Importamos el decorador login_required de flask_security
from flask_security.decorators import roles_required
#Importamos el objeto de la BD desde __init__.py
from . import db
from . forms import UseForm
from . models import Producto
from flask import request
from flask import redirect, render_template, url_for



main = Blueprint('main',__name__)

#Definimos la ruta a la página principal
@main.route('/')
def index():
    return render_template('index.html')

#Definimos la ruta a la página de perfil
@main.route('/profile')
@login_required
#@roles_required('admin','user')
def profile():
    create_forms=UseForm(request.form)
    productosAll=Producto.query.all()
    if current_user.roles[0].name=="admin":
        admin=True
        return render_template('ABCompleto.html',form=create_forms,productos=productosAll,admin=admin)

    else:
        admin=False
        return render_template('profile.html',name=current_user.name,admin=admin)    

@main.route('/productosMenu')
@login_required
@roles_required('user')
def productosMenu():
        productosAll=Producto.query.all()
        return render_template('productos.html',productos=productosAll)



@main.route("/agregar",methods=['GET','POST'])
def agregar():
    create_forms=UseForm(request.form)
    if request.method=='POST':
        product= Producto(nombreProducto=create_forms.nombreProducto.data,
                       precio=create_forms.precio.data,
                       marca=create_forms.marca.data,
                       cantidad=create_forms.cantidad.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('main.profile'))
    return render_template('formAgregar.html',form=create_forms)


@main.route("/modificar",methods=['GET','POST'])
def modificar():
    create_forms=UseForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        product= db.session.query(Producto).filter(Producto.id==id).first()
        create_forms.id.data=product.id
        create_forms.nombreProducto.data= product.nombreProducto
        create_forms.precio.data= product.precio
        create_forms.marca.data= product.marca
        create_forms.cantidad.data= product.cantidad


    if request.method=='POST':
        id=create_forms.id.data
        product= db.session.query(Producto).filter(Producto.id==id).first()
        product.id=create_forms.id.data
        product.nombreProducto=create_forms.nombreProducto.data
        product.precio=create_forms.precio.data
        product.marca=create_forms.marca.data
        product.cantidad=create_forms.cantidad.data

        db.session.add(product)
        db.session.commit()
        return redirect(url_for('main.profile'))

    return render_template('modificar.html',form=create_forms)

@main.route("/eliminar")
def eliminar():
        id=request.args.get('id')

        product= db.session.query(Producto).filter(Producto.id==id).first()
        db.session.delete(product)
        db.session.commit()
        flash("Se ha eliminado el producto")
        return redirect(url_for('main.profile'))



