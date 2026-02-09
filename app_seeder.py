# Seeder para poblar la base de datos con productos de ejemplo

productos_ejemplo = [
    ("Laptop HP", 12999.99, 15, True, "Computadoras"),
    ("Mouse Logitech", 299.50, 50, True, "Accesorios"),
    ("Teclado Mecanico", 899.00, 30, True, "Accesorios"),
    ("Monitor Samsung 24\"", 3499.00, 20, True, "Computadoras"),
    ("Audifonos Bluetooth", 599.99, 45, True, "Audio"),
    ("Webcam HD", 450.00, 25, False, "Accesorios"),
    ("USB 32GB", 89.90, 100, True, "Almacenamiento"),
    ("Disco Duro 1TB", 1299.00, 18, True, "Almacenamiento"),
    ("Cargador Universal", 199.50, 60, True, "Accesorios"),
    ("Cable HDMI 2m", 79.00, 80, False, "Cables"),
]

def seed():
    from repositories import ProductosRepository
    from services import ProductosService
    
    ProductosRepository.crear_tabla()
    
    # Verificar si ya hay productos
    if ProductosService.contar() > 0:
        print("La base de datos ya tiene productos.")
        return
    
    # Insertar productos
    for nombre, precio, stock, activo, categoria in productos_ejemplo:
        ProductosService.crear(nombre, precio, stock, activo, categoria)
        print(f"Agregado: {nombre}")
    
    print("\nSeeder completado! 10 productos agregados.")

if __name__ == '__main__':
    seed()
