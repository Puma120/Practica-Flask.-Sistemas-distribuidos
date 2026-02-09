# Servicio de Autenticacion - Logica de negocio
from flask import session

# Usuario ficticio (hardcoded)
USUARIO = 'admin'
PASSWORD = '1234'

class AuthService:
    
    @staticmethod
    def login(usuario, password):
        if usuario == USUARIO and password == PASSWORD:
            session['usuario'] = usuario
            return True, 'Bienvenido!'
        return False, 'Usuario o contrasena incorrectos'
    
    @staticmethod
    def logout():
        session.pop('usuario', None)
        return True, 'Sesion cerrada'
    
    @staticmethod
    def esta_autenticado():
        return 'usuario' in session
    
    @staticmethod
    def obtener_usuario():
        return session.get('usuario', None)
