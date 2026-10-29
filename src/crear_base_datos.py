import sqlite3

conexion = sqlite3.connect("accesos.db")
cursor = conexion.cursor()

# Tabla de usuarios registrados
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    categoria TEXT NOT NULL,
    fecha_registro TEXT DEFAULT (datetime('now', 'localtime'))
)
""")

# Tabla de eventos de acceso (cada vez que el sistema reconoce o no a alguien)
cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos_acceso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    categoria TEXT,
    resultado TEXT NOT NULL,
    distancia REAL,
    fecha_hora TEXT DEFAULT (datetime('now', 'localtime'))
)
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente: accesos.db")