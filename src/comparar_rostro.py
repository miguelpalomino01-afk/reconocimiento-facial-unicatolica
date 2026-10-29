import face_recognition
import cv2
import pickle
import numpy as np

ARCHIVO_EMBEDDINGS = "dataset/embeddings.pkl"
UMBRAL_TOLERANCIA = 0.6  # más bajo = más estricto

# Cargar los embeddings guardados
with open(ARCHIVO_EMBEDDINGS, "rb") as f:
    embeddings_conocidos = pickle.load(f)

# Aplanar la estructura: lista de (nombre, vector) para comparar uno por uno
nombres = []
vectores = []
for persona, lista_vectores in embeddings_conocidos.items():
    for vector in lista_vectores:
        nombres.append(persona)
        vectores.append(vector)

print(f"Personas cargadas: {set(nombres)}")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo acceder a la cámara")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # OpenCV usa BGR, face_recognition espera RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        ubicaciones = face_recognition.face_locations(rgb_frame)
        codificaciones = face_recognition.face_encodings(rgb_frame, ubicaciones)

        for (top, right, bottom, left), codificacion in zip(ubicaciones, codificaciones):
            distancias = face_recognition.face_distance(vectores, codificacion)

            nombre_resultado = "No reconocido"
            color = (0, 0, 255)  # rojo

            if len(distancias) > 0:
                mejor_indice = np.argmin(distancias)
                if distancias[mejor_indice] <= UMBRAL_TOLERANCIA:
                    nombre_resultado = nombres[mejor_indice]
                    color = (0, 255, 0)  # verde

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, nombre_resultado, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow('Comparacion de rostro - presiona Q para salir', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()