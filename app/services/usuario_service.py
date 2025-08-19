from sqlalchemy.orm import Session
import os
import uuid
import numpy as np
from fastapi import UploadFile
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate
import face_recognition
from PIL import Image
from io import BytesIO

UPLOAD_DIR = "imagenes_rostros"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def crear_usuario(db: Session, nombre: str, imagen: UploadFile):
    try:
        contenido = imagen.file.read()
        img = Image.open(BytesIO(contenido)).convert("RGB")
        np_img = np.array(img)
        codificaciones = face_recognition.face_encodings(np_img)

        if not codificaciones:
            raise ValueError("No se detectó ningún rostro en la imagen")

        codificacion = codificaciones[0]

        # 🟢 Nombre único para imagen, sin extensión
        filename_base = uuid.uuid4().hex
        filename = f"{filename_base}.jpg"
        ruta_imagen = os.path.join(UPLOAD_DIR, filename)
        img.save(ruta_imagen)

        db_usuario = Usuario(
            nombre=nombre,
            codificacion=codificacion.tobytes(),
            imagen_path=filename_base  # 🟢 Guardamos solo el nombre base para compararlo luego
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    except Exception as e:
        raise RuntimeError(f"Error al registrar usuario: {str(e)}")


def obtener_usuarios(db: Session):
    return db.query(Usuario).all()


def verificar_facial(db: Session, imagen: UploadFile):
    try:
        contenido = imagen.file.read()
        img = Image.open(BytesIO(contenido)).convert("RGB")
        np_img = np.array(img)

        codificaciones = face_recognition.face_encodings(np_img)
        if not codificaciones:
            raise ValueError("No se detectó ningún rostro en la imagen")

        codificacion_actual = codificaciones[0]

        usuarios = obtener_usuarios(db)
        for usuario in usuarios:
            codificacion_guardada = np.frombuffer(usuario.codificacion, dtype=np.float64)

            resultados = face_recognition.compare_faces(
                [codificacion_guardada],
                codificacion_actual,
                tolerance=0.45
            )

            if resultados[0]:
                return usuario

        return None

    except Exception as e:
        raise RuntimeError(f"Error en el reconocimiento facial: {str(e)}")