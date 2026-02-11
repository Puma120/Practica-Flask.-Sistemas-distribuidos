# API - Rutas de Productos
from flask import Blueprint, request, jsonify, session
from services import ProductosService
from functools import wraps

api_productos_bp = Blueprint('api_productos', __name__, url_prefix='/api/productos')


# Convierte un producto (sqlite3.Row) a diccionario
def producto_a_dict(p):
    return {
        'id': p['id'],
        'nombre': p['nombre'],
        'precio': p['precio'],
        'stock': p['stock'],
        'activo': bool(p['activo']),
        'categoria': p['categoria']
    }


# Decorador para proteger rutas de la API
def api_login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return jsonify({'error': 'No autenticado'}), 401
        return f(*args, **kwargs)
    return decorated_function


# GET /api/productos - Listar todos
@api_productos_bp.route('', methods=['GET'])
@api_login_requerido
def listar():
    productos = ProductosService.listar()
    resultado = [producto_a_dict(p) for p in productos]
    return jsonify({'mensaje': 'Lista de productos', 'total': len(resultado), 'productos': resultado}), 200


# GET /api/productos/<id> - Obtener uno
@api_productos_bp.route('/<int:id>', methods=['GET'])
@api_login_requerido
def obtener(id):
    producto = ProductosService.obtener(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify({'mensaje': 'Producto encontrado', 'producto': producto_a_dict(producto)}), 200


# POST /api/productos - Crear
@api_productos_bp.route('', methods=['POST'])
@api_login_requerido
def crear():
    datos = request.get_json()

    if not datos:
        return jsonify({'error': 'Se requiere JSON con datos del producto'}), 400

    nombre = datos.get('nombre', '').strip()
    precio = datos.get('precio', 0)
    stock = datos.get('stock', 0)
    activo = datos.get('activo', True)
    categoria = datos.get('categoria', 'General').strip()

    resultado, error = ProductosService.crear(nombre, precio, stock, activo, categoria)

    if error:
        return jsonify({'error': error}), 400

    nuevo = ProductosService.obtener(resultado)
    return jsonify({'mensaje': 'Producto creado', 'producto': producto_a_dict(nuevo)}), 201


# PUT /api/productos/<id> - Actualizar
@api_productos_bp.route('/<int:id>', methods=['PUT'])
@api_login_requerido
def actualizar(id):
    producto = ProductosService.obtener(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    datos = request.get_json()
    if not datos:
        return jsonify({'error': 'Se requiere JSON con datos del producto'}), 400

    nombre = datos.get('nombre', producto['nombre']).strip()
    precio = datos.get('precio', producto['precio'])
    stock = datos.get('stock', producto['stock'])
    activo = datos.get('activo', bool(producto['activo']))
    categoria = datos.get('categoria', producto['categoria']).strip()

    resultado, error = ProductosService.actualizar(id, nombre, precio, stock, activo, categoria)

    if error:
        return jsonify({'error': error}), 400

    actualizado = ProductosService.obtener(id)
    return jsonify({'mensaje': 'Producto actualizado', 'producto': producto_a_dict(actualizado)}), 200


# DELETE /api/productos/<id> - Eliminar
@api_productos_bp.route('/<int:id>', methods=['DELETE'])
@api_login_requerido
def eliminar(id):
    producto = ProductosService.obtener(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    eliminado = producto_a_dict(producto)
    ProductosService.eliminar(id)
    return jsonify({'mensaje': 'Producto eliminado', 'producto': eliminado}), 200
