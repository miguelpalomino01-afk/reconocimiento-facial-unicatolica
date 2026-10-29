import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo acceder a la cámara")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Prueba de camara - presiona Q para salir', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()