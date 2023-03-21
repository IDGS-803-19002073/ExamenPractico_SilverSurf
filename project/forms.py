from wtforms import Form
from wtforms import StringField,IntegerField
from wtforms import EmailField
from wtforms import validators


class UseForm(Form):
    id=IntegerField('id')
    nombreProducto=StringField('nombreProducto')
    precio=StringField('precio')
    marca=StringField('marca')
    cantidad=StringField('cantidad')