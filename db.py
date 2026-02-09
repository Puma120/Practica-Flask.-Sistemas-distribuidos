# db.py - Conexion y creacion de tablas
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


