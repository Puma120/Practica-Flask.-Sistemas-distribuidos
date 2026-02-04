# db.py - Logica de base de datos con sqlite3 puro
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'productos.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn

def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            activo INTEGER DEFAULT 1,
            categoria TEXT DEFAULT 'General'
        )
    ''')
    conn.commit()
    conn.close()

# Funciones CRUD
def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM producto')
    productos = cursor.fetchall()
    conn.close()
    return productos

def obtener_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM producto WHERE id = ?', (id,))
    producto = cursor.fetchone()
    conn.close()
    return producto

def agregar_producto(nombre, precio, stock, activo, categoria):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO producto (nombre, precio, stock, activo, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, precio, stock, int(activo), categoria))
    conn.commit()
    conn.close()

def actualizar_producto(id, nombre, precio, stock, activo, categoria):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE producto SET nombre=?, precio=?, stock=?, activo=?, categoria=?
        WHERE id=?
    ''', (nombre, precio, stock, int(activo), categoria, id))
    conn.commit()
    conn.close()

def eliminar_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM producto WHERE id=?', (id,))
    conn.commit()
    conn.close()


