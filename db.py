# db.py - Lógica de base de datos compartida
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo Producto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    activo = db.Column(db.Boolean, default=True)

# Funciones CRUD
def obtener_productos():
    return Producto.query.all()

def obtener_producto(id):
    return Producto.query.get_or_404(id)

def agregar_producto(nombre, precio, stock, activo):
    producto = Producto(nombre=nombre, precio=precio, stock=stock, activo=activo)
    db.session.add(producto)
    db.session.commit()
    return producto

def actualizar_producto(id, nombre, precio, stock, activo):
    producto = Producto.query.get_or_404(id)
    producto.nombre = nombre
    producto.precio = precio
    producto.stock = stock
    producto.activo = activo
    db.session.commit()
    return producto

def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()


