# servidor.py
from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
DATABASE = 'tareas.db'

# --- Configuración de Base de Datos ---
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # Creamos la tabla de usuarios si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- ENDPOINTS ---

# 1. Registro de Usuarios
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    if not data or 'usuario' not in data or 'contrasena' not in data:
        return jsonify({"error": "Faltan datos (usuario y contrasena)"}), 400

    usuario = data['usuario']
    contrasena = data['contrasena']

    # Hashear la contraseña (¡Nunca en texto plano!)
    contrasena_hash = generate_password_hash(contrasena)

    conn = get_db()
    try:
        conn.execute('INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)',
                    (usuario, contrasena_hash))
        conn.commit()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409
    finally:
        conn.close()

# 2. Inicio de Sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'usuario' not in data or 'contrasena' not in data:
        return jsonify({"error": "Faltan credenciales"}), 400

    usuario = data['usuario']
    contrasena = data['contrasena']

    conn = get_db()
    user = conn.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,)).fetchone()
    conn.close()

    if user and check_password_hash(user['contrasena'], contrasena):
        # Generamos un token simple para simular el acceso a las tareas
        token = secrets.token_hex(16)
        return jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "token": token,
            "acceso": "Permitido"
        }), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

# 3. Gestión de Tareas (HTML de bienvenida)
@app.route('/tareas', methods=['GET'])
def tareas():
    # Nota: El PDF indica mostrar un HTML de bienvenida para este endpoint.
    html_bienvenida = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Panel de Tareas</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }
            h1 { color: #333; }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>¡Bienvenido al Sistema de Gestión de Tareas!</h1>
            <p>Has accedido correctamente al panel. Aquí podrás gestionar tus pendientes.</p>
        </div>
    </body>
    </html>
    """
    return html_bienvenida

if __name__ == '__main__':
    init_db()
    print("Servidor iniciado en http://127.0.0.1:5000")
    app.run(debug=True)