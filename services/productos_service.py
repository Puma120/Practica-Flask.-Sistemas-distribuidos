# Servicio de Productos - Logica de negocio
from repositories import ProductosRepository

class ProductosService:
    
    @staticmethod
    def listar():
        return ProductosRepository.obtener_todos()
    
    @staticmethod
    def obtener(id):
        return ProductosRepository.obtener_por_id(id)
    
    @staticmethod
    def crear(nombre, precio, stock, activo, categoria):
        # Validaciones
        errores = ProductosService._validar(nombre, precio, stock)
        if errores:
            return None, errores
        
        nuevo_id = ProductosRepository.insertar(nombre, float(precio), int(stock), activo, categoria)
        return nuevo_id, None
    
    @staticmethod
    def actualizar(id, nombre, precio, stock, activo, categoria):
        # Validaciones
        errores = ProductosService._validar(nombre, precio, stock)
        if errores:
            return None, errores
        
        ProductosRepository.actualizar(id, nombre, float(precio), int(stock), activo, categoria)
        return True, None
    
    @staticmethod
    def eliminar(id):
        ProductosRepository.eliminar(id)
        return True
    
    @staticmethod
    def contar():
        return ProductosRepository.contar()
    
    @staticmethod
    def _validar(nombre, precio, stock):
        if not nombre or not nombre.strip():
            return 'El nombre es requerido'
        try:
            precio = float(precio)
            stock = int(stock)
            if precio < 0 or stock < 0:
                return 'Precio y stock deben ser no negativos'
        except:
            return 'Precio y stock deben ser numeros no negativos'
        return None

