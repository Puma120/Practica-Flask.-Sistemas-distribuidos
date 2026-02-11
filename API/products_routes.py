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


# GET /api/productos - Listar con filtros y paginacion
# Filtros: nombre, categoria, precio_min, precio_max, activo
# Paginacion: page (default 1), per_page (default 10)
@api_productos_bp.route('', methods=['GET'])
@api_login_requerido
def listar():
    productos = ProductosService.listar()
    resultado = [producto_a_dict(p) for p in productos]

    # Filtros
    nombre = request.args.get('nombre', '').strip().lower()
    categoria = request.args.get('categoria', '').strip().lower()
    precio_min = request.args.get('precio_min', type=float)
    precio_max = request.args.get('precio_max', type=float)
    activo = request.args.get('activo')

    if nombre:
        resultado = [p for p in resultado if nombre in p['nombre'].lower()]
    if categoria:
        resultado = [p for p in resultado if categoria in p['categoria'].lower()]
    if precio_min is not None:
        resultado = [p for p in resultado if p['precio'] >= precio_min]
    if precio_max is not None:
        resultado = [p for p in resultado if p['precio'] <= precio_max]
    if activo is not None:
        activo_bool = activo.lower() in ('true', '1', 'si')
        resultado = [p for p in resultado if p['activo'] == activo_bool]

    total_filtrado = len(resultado)

    # Paginacion
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10
    if per_page > 100:
        per_page = 100

    inicio = (page - 1) * per_page
    fin = inicio + per_page
    productos_paginados = resultado[inicio:fin]
    total_paginas = (total_filtrado + per_page - 1) // per_page if total_filtrado > 0 else 1

    return jsonify({
        'mensaje': 'Lista de productos',
        'paginacion': {
            'page': page,
            'per_page': per_page,
            'total': total_filtrado,
            'total_paginas': total_paginas
        },
        'productos': productos_paginados
    }), 200


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
