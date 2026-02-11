# Pablo Urbina Macip
# API REST con Flask - Reutiliza la arquitectura por capas existente
# Endpoints JSON para CRUD de Productos y Autenticacion

import sys
import os

# Agregar el directorio raiz al path para importar las capas existentes
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify
from repositories import ProductosRepository
from API import api_productos_bp, api_auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_123'

# Ruta de bienvenida
@app.route('/')
def bienvenida():
    return jsonify({
        'mensaje': 'Bienvenido a la API de Pablo Urbina Macip',
        'endpoints': {
            'auth': '/api/auth (login, logout, estado)',
            'productos': '/api/productos (CRUD)'
        }
    }), 200

# Registrar Blueprints de la API
app.register_blueprint(api_productos_bp)
app.register_blueprint(api_auth_bp)

if __name__ == '__main__':
    ProductosRepository.crear_tabla()

    from services import ProductosService
    if ProductosService.contar() == 0:
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from app_seeder import productos_ejemplo
        for nombre, precio, stock, activo, categoria in productos_ejemplo:
            ProductosService.crear(nombre, precio, stock, activo, categoria)
        print("Seeder ejecutado: 10 productos agregados.")

    print("\n--- API REST disponible ---")
    print("POST   /api/auth/login")
    print("POST   /api/auth/logout")
    print("GET    /api/auth/estado")
    print("GET    /api/productos")
    print("GET    /api/productos/<id>")
    print("POST   /api/productos")
    print("PUT    /api/productos/<id>")
    print("DELETE /api/productos/<id>")
    print("---------------------------\n")

    app.run(debug=True, port=5050)
