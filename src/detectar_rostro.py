import cv2

# Cargar el clasificador de rostros que viene incluido en OpenCV
face_cascade = cv2.CascadeClassifier('recursos/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo acceder a la cámara")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir a escala de grises (el detector trabaja mejor así)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostros en el frame
        rostros = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
        )

        # Dibujar un rectángulo alrededor de cada rostro detectado
        for (x, y, w, h) in rostros:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Rostro detectado', (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow('Deteccion de rostro - presiona Q para salir', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()