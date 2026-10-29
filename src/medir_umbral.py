import face_recognition
import cv2
import pickle
import numpy as np

ARCHIVO_EMBEDDINGS = "dataset/embeddings.pkl"

with open(ARCHIVO_EMBEDDINGS, "rb") as f:
    embeddings_conocidos = pickle.load(f)

nombres = []
vectores = []
for persona, lista_vectores in embeddings_conocidos.items():
    for vector in lista_vectores:
        nombres.append(persona)
        vectores.append(vector)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    ubicaciones = face_recognition.face_locations(rgb_frame)
    codificaciones = face_recognition.face_encodings(rgb_frame, ubicaciones)

    for (top, right, bottom, left), codificacion in zip(ubicaciones, codificaciones):
        distancias = face_recognition.face_distance(vectores, codificacion)

        # Mostrar la distancia contra CADA persona del dataset, no solo la mejor
        y_texto = top - 10
        for nombre, distancia in zip(nombres, distancias):
            texto = f"{nombre}: {distancia:.3f}"
            cv2.putText(frame, texto, (left, y_texto),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            y_texto -= 20

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow('Medicion de distancias - presiona Q para salir', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()