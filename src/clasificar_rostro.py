import face_recognition
import cv2
import pickle
import json
import sqlite3
import numpy as np
import time

ARCHIVO_EMBEDDINGS = "dataset/embeddings.pkl"
ARCHIVO_CATEGORIAS = "dataset/categorias.json"
BASE_DATOS = "accesos.db"
UMBRAL_TOLERANCIA = 0.6
SEGUNDOS_ENTRE_REGISTROS = 5  # evita guardar el mismo evento decenas de veces por segundo

with open(ARCHIVO_EMBEDDINGS, "rb") as f:
    embeddings_conocidos = pickle.load(f)

with open(ARCHIVO_CATEGORIAS, "r", encoding="utf-8") as f:
    categorias = json.load(f)

nombres = []
vectores = []
for persona, lista_vectores in embeddings_conocidos.items():
    for vector in lista_vectores:
        nombres.append(persona)
        vectores.append(vector)

def registrar_evento(nombre, categoria, resultado, distancia):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO eventos_acceso (nombre, categoria, resultado, distancia) VALUES (?, ?, ?, ?)",
        (nombre, categoria, resultado, distancia)
    )
    conexion.commit()
    conexion.close()

ultimo_registro = 0

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo acceder a la cámara")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ubicaciones = face_recognition.face_locations(rgb_frame)
        codificaciones = face_recognition.face_encodings(rgb_frame, ubicaciones)

        for (top, right, bottom, left), codificacion in zip(ubicaciones, codificaciones):
            distancias = face_recognition.face_distance(vectores, codificacion)

            etiqueta = "No reconocido"
            color = (0, 0, 255)
            nombre_bd = None
            categoria_bd = None
            distancia_bd = None
            resultado_bd = "no_reconocido"

            if len(distancias) > 0:
                mejor_indice = np.argmin(distancias)
                distancia_bd = float(distancias[mejor_indice])

                if distancias[mejor_indice] <= UMBRAL_TOLERANCIA:
                    nombre_bd = nombres[mejor_indice]
                    categoria_bd = categorias.get(nombre_bd, "sin categoria")
                    etiqueta = f"{nombre_bd} - {categoria_bd}"
                    color = (0, 255, 0)
                    resultado_bd = "reconocido"

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, etiqueta, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # Registrar el evento, con un pequeño límite para no saturar la base de datos
            ahora = time.time()
            if ahora - ultimo_registro >= SEGUNDOS_ENTRE_REGISTROS:
                registrar_evento(nombre_bd, categoria_bd, resultado_bd, distancia_bd)
                ultimo_registro = ahora

        cv2.imshow('Clasificacion con registro - presiona Q para salir', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()