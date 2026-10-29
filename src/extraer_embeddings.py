import face_recognition
import os
import pickle
from PIL import Image, ImageOps
import numpy as np

RUTA_DATASET = "dataset"
ARCHIVO_SALIDA = "dataset/embeddings.pkl"

embeddings_conocidos = {}

for persona in os.listdir(RUTA_DATASET):
    carpeta_persona = os.path.join(RUTA_DATASET, persona)

    if not os.path.isdir(carpeta_persona):
        continue

    print(f"Procesando: {persona}")
    vectores_persona = []

    for archivo in os.listdir(carpeta_persona):
        ruta_imagen = os.path.join(carpeta_persona, archivo)

        try:
            # Abrir con Pillow y corregir la rotación según los metadatos EXIF
            imagen_pil = Image.open(ruta_imagen)
            imagen_pil = ImageOps.exif_transpose(imagen_pil)
            imagen_pil = imagen_pil.convert("RGB")
            imagen = np.array(imagen_pil)

            print(f"  Tamaño de la imagen: {imagen.shape}")

            # Aumentar upsampling ayuda a detectar rostros pequeños o menos nítidos
            ubicaciones = face_recognition.face_locations(imagen, number_of_times_to_upsample=2)

            if len(ubicaciones) == 0:
                print(f"  No se detectó rostro en: {archivo} (aunque se corrigió orientación)")
                continue

            codificaciones = face_recognition.face_encodings(imagen, known_face_locations=ubicaciones)
            vectores_persona.append(codificaciones[0])
            print(f"  Rostro codificado: {archivo}")

        except Exception as e:
            print(f"  Error procesando {archivo}: {e}")

    if vectores_persona:
        embeddings_conocidos[persona] = vectores_persona

with open(ARCHIVO_SALIDA, "wb") as f:
    pickle.dump(embeddings_conocidos, f)

print(f"\nListo. Se guardaron embeddings de {len(embeddings_conocidos)} personas en {ARCHIVO_SALIDA}")