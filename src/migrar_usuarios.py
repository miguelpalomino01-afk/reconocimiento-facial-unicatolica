import sqlite3
import json

with open("dataset/categorias.json", "r", encoding="utf-8") as f:
    categorias = json.load(f)

conexion = sqlite3.connect("accesos.db")
cursor = conexion.cursor()

for nombre, categoria in categorias.items():
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, categoria) VALUES (?, ?)",
            (nombre, categoria)
        )
        print(f"Usuario agregado: {nombre} - {categoria}")
    except sqlite3.IntegrityError:
        print(f"Usuario ya existía, se omitió: {nombre}")

conexion.commit()
conexion.close()

# Verificación: mostrar todos los usuarios guardados
conexion = sqlite3.connect("accesos.db")
cursor = conexion.cursor()
cursor.execute("SELECT * FROM usuarios")
print("\nUsuarios en la base de datos:")
for fila in cursor.fetchall():
    print(fila)
conexion.close()