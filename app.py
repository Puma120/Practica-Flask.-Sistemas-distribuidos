# Pablo Urbina Macip
# Practica Flask: CRUD Producto con login ficticio y SQLite
# Arquitectura por capas: Repository -> Service -> Routes

from flask import Flask
from routes import productos_bp, auth_bp
from repositories import ProductosRepository

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_123'

# Registrar Blueprints
app.register_blueprint(productos_bp)
app.register_blueprint(auth_bp)

# Crear tablas e iniciar app
if __name__ == '__main__':
    ProductosRepository.crear_tabla()
    
    from services import ProductosService
    if ProductosService.contar() == 0:
        from app_seeder import productos_ejemplo
        for nombre, precio, stock, activo, categoria in productos_ejemplo:
            ProductosService.crear(nombre, precio, stock, activo, categoria)
        print("Seeder ejecutado: 10 productos agregados.")
    
    app.run(debug=True)
