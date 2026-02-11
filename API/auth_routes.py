# API - Rutas de Autenticacion
from flask import Blueprint, request, jsonify
from services import AuthService

api_auth_bp = Blueprint('api_auth', __name__, url_prefix='/api/auth')


# POST /api/auth/login
@api_auth_bp.route('/login', methods=['POST'])
def login():
    datos = request.get_json()

    if not datos or 'usuario' not in datos or 'password' not in datos:
        return jsonify({'error': 'Se requiere usuario y password'}), 400

    exito, mensaje = AuthService.login(datos['usuario'], datos['password'])

    if exito:
        return jsonify({'mensaje': mensaje, 'usuario': datos['usuario']}), 200
    return jsonify({'error': mensaje}), 401


# POST /api/auth/logout
@api_auth_bp.route('/logout', methods=['POST'])
def logout():
    exito, mensaje = AuthService.logout()
    return jsonify({'mensaje': mensaje}), 200


# GET /api/auth/estado
@api_auth_bp.route('/estado', methods=['GET'])
def estado():
    if AuthService.esta_autenticado():
        return jsonify({
            'autenticado': True,
            'usuario': AuthService.obtener_usuario()
        }), 200
    return jsonify({'autenticado': False}), 200
