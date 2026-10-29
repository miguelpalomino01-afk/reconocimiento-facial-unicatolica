import sqlite3
import matplotlib.pyplot as plt

conexion = sqlite3.connect("accesos.db")
cursor = conexion.cursor()

# --- Gráfico 1: accesos por categoría (reconocidos) + no reconocidos ---
cursor.execute("""
    SELECT categoria, COUNT(*) 
    FROM eventos_acceso 
    WHERE resultado = 'reconocido' 
    GROUP BY categoria
""")
datos_categoria = cursor.fetchall()

cursor.execute("""
    SELECT COUNT(*) FROM eventos_acceso WHERE resultado = 'no_reconocido'
""")
total_no_reconocidos = cursor.fetchone()[0]

etiquetas = [fila[0] for fila in datos_categoria] + ["No reconocido"]
valores = [fila[1] for fila in datos_categoria] + [total_no_reconocidos]
colores = ["#4CAF50"] * len(datos_categoria) + ["#E53935"]

fig, axs = plt.subplots(1, 2, figsize=(12, 5))

axs[0].bar(etiquetas, valores, color=colores)
axs[0].set_title("Eventos de acceso por categoría")
axs[0].set_ylabel("Cantidad de eventos")
axs[0].tick_params(axis='x', rotation=20)

# --- Gráfico 2: accesos por hora del día ---
cursor.execute("""
    SELECT strftime('%H', fecha_hora) as hora, COUNT(*) 
    FROM eventos_acceso 
    GROUP BY hora 
    ORDER BY hora
""")
datos_hora = cursor.fetchall()
horas = [f"{fila[0]}:00" for fila in datos_hora]
cantidades = [fila[1] for fila in datos_hora]

axs[1].bar(horas, cantidades, color="#1E88E5")
axs[1].set_title("Eventos de acceso por hora del día")
axs[1].set_ylabel("Cantidad de eventos")

plt.tight_layout()
plt.savefig("reporte_accesos.png", dpi=150)
plt.show()

conexion.close()
print("Gráfico guardado como reporte_accesos.png")