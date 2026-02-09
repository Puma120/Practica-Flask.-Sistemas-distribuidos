# Rutas de Productos - Capa de presentacion
from flask import Blueprint, render_template, request, redirect, url_for, flash
from services import ProductosService
from functools import wraps
from flask import session

productos_bp = Blueprint('productos', __name__)

# Decorador para proteger rutas
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash('Debes iniciar sesion', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta principal - Redirige a productos
@productos_bp.route('/')
@login_requerido
def index():
    return redirect(url_for('productos.listar_productos'))

# Crear producto
@productos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_requerido
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        precio = request.form['precio']
        stock = request.form['stock']
        activo = 'activo' in request.form
        categoria = request.form.get('categoria', 'General').strip()
        
        resultado, error = ProductosService.crear(nombre, precio, stock, activo, categoria)
        
        if error:
            flash(error, 'error')
            return render_template('index.html')
        
        flash('Producto creado', 'success')
        return redirect(url_for('productos.listar_productos'))
    return render_template('index.html')

# Listar productos
@productos_bp.route('/productos')
@login_requerido
def listar_productos():
    productos = ProductosService.listar()
    return render_template('products.html', productos=productos)

# Editar producto
@productos_bp.route('/productos/<int:id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_producto(id):
    producto = ProductosService.obtener(id)
    
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        precio = request.form['precio']
        stock = request.form['stock']
        activo = 'activo' in request.form
        categoria = request.form.get('categoria', 'General').strip()
        
        resultado, error = ProductosService.actualizar(id, nombre, precio, stock, activo, categoria)
        
        if error:
            flash(error, 'error')
            return render_template('form.html', producto=producto)
        
        flash('Producto actualizado', 'success')
        return redirect(url_for('productos.listar_productos'))
    return render_template('form.html', producto=producto)

# Eliminar producto
@productos_bp.route('/productos/<int:id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_producto_route(id):
    ProductosService.eliminar(id)
    flash('Producto eliminado', 'success')
    return redirect(url_for('productos.listar_productos'))
