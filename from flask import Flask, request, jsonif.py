from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Fase de Diseño y Base de datos
def init_db():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Fase de Desarrollo: Rutas y Lógica
@app.route('/')
def index():
    return """
    <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 100px;">
        <h1 style="color: #2c3e50;">Sistema de Gestión de Inventario</h1>
        <h3>Prototipo Funcional</h3>
        <p><b>Desarrollado por:</b> Edwin Alexander Zarate Pérez</p>
    </div>
    """

@app.route('/api/productos', methods=['GET'])
def get_productos():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return jsonify(productos)

@app.route('/api/add', methods=['POST'])
def add_producto():
    data = request.get_json()
    # Fase de Calidad y Pruebas: Validación de datos
    if not data or not 'nombre' in data or not 'cantidad' in data:
        return jsonify({"error": "Faltan datos requeridos"}), 400
    
    try:
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                       (data['nombre'], data['cantidad'], data['precio']))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Producto agregado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    # Ejecución del servidor local
    app.run(debug=True)