# Pablo Urbina Macip
# Practica Flask: CRUD Producto con login ficticio y SQLite
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from db import crear_tablas, obtener_producto, obtener_productos, agregar_producto, actualizar_producto, eliminar_producto

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_123'

# Usuario ficticio
USUARIO = 'admin'
PASSWORD = '1234'

# Decorador para proteger rutas
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash('Debes iniciar sesión', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta principal - Redirige a productos
@app.route('/')
@login_requerido
def index():
    return redirect(url_for('listar_productos'))

# Crear producto (index.html)
@app.route('/nuevo', methods=['GET', 'POST'])
@login_requerido
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        precio = request.form['precio']
        stock = request.form['stock']
        activo = 'activo' in request.form
        categoria = request.form.get('categoria', 'General').strip()
        
        # Validaciones
        if not nombre:
            flash('El nombre es requerido', 'error')
            return render_template('index.html')
        try:
            precio = float(precio)
            stock = int(stock)
            if precio < 0 or stock < 0:
                raise ValueError()
        except:
            flash('Precio y stock deben ser números no negativos', 'error')
            return render_template('index.html')
        
        agregar_producto(nombre, precio, stock, activo, categoria)
        flash('Producto creado', 'success')
        return redirect(url_for('listar_productos'))
    return render_template('index.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        if usuario == USUARIO and password == PASSWORD:
            session['usuario'] = usuario
            flash('Bienvenido!', 'success')
            return redirect(url_for('listar_productos'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada', 'success')
    return redirect(url_for('login'))

# CRUD - Listar productos
@app.route('/productos')
@login_requerido
def listar_productos():
    productos = obtener_productos()
    return render_template('products.html', productos=productos)

# CRUD - Editar producto
@app.route('/productos/<int:id>/editar', methods=['GET', 'POST'])
@login_requerido
def editar_producto(id):
    producto = obtener_producto(id)
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        precio = request.form['precio']
        stock = request.form['stock']
        activo = 'activo' in request.form
        categoria = request.form.get('categoria', 'General').strip()
        
        # Validaciones
        if not nombre:
            flash('El nombre es requerido', 'error')
            return render_template('form.html', producto=producto)
        try:
            precio = float(precio)
            stock = int(stock)
            if precio < 0 or stock < 0:
                raise ValueError()
        except:
            flash('Precio y stock deben ser números no negativos', 'error')
            return render_template('form.html', producto=producto)
        
        actualizar_producto(id, nombre, precio, stock, activo, categoria)
        flash('Producto actualizado', 'success')
        return redirect(url_for('listar_productos'))
    return render_template('form.html', producto=producto)

# CRUD - Eliminar producto
@app.route('/productos/<int:id>/eliminar', methods=['POST'])
@login_requerido
def eliminar_producto_route(id):
    eliminar_producto(id)
    flash('Producto eliminado', 'success')
    return redirect(url_for('listar_productos'))

# Crear tablas e iniciar app
if __name__ == '__main__':
    crear_tablas()
    # Seed automatico si no hay productos
    if len(obtener_productos()) == 0:
        from app_seeder import productos_ejemplo
        for nombre, precio, stock, activo, categoria in productos_ejemplo:
            agregar_producto(nombre, precio, stock, activo, categoria)
        print("Seeder ejecutado: 10 productos agregados.")
    app.run(debug=True)
