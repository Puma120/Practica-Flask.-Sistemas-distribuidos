# Rutas de Autenticacion - Capa de presentacion
from flask import Blueprint, render_template, request, redirect, url_for, flash
from services import AuthService

auth_bp = Blueprint('auth', __name__)

# Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        
        exito, mensaje = AuthService.login(usuario, password)
        
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('productos.listar_productos'))
        else:
            flash(mensaje, 'error')
    
    return render_template('login.html')

# Logout
@auth_bp.route('/logout')
def logout():
    exito, mensaje = AuthService.logout()
    flash(mensaje, 'success')
    return redirect(url_for('auth.login'))
