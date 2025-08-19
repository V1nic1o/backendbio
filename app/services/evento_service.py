import os
import face_recognition
from fastapi import UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.evento_model import Evento
from app.models.usuario_model import Usuario

# Ruta a las imágenes registradas
RUTA_IMAGENES = "imagenes_rostros"

def registrar_evento(db: Session, usuario_id: int, tipo: str):
    ahora = datetime.now()
    nuevo_evento = Evento(
        usuario_id=usuario_id,
        tipo=tipo,
        fecha=ahora.date(),
        hora=ahora.time(),
        timestamp=ahora.timestamp()
    )
    db.add(nuevo_evento)
    db.commit()
    db.refresh(nuevo_evento)
    return nuevo_evento

def obtener_eventos(db: Session):
    return db.query(Evento).all()

async def registrar_evento_con_rostro(db: Session, file: UploadFile):
    contenido = await file.read()

    # Cargar imagen enviada
    imagen_desconocida = face_recognition.load_image_file(file.file)
    rostros_desconocidos = face_recognition.face_encodings(imagen_desconocida)

    if not rostros_desconocidos:
        raise ValueError("No se detectó ningún rostro en la imagen")

    encoding_desconocido = rostros_desconocidos[0]

    # Recorrer las imágenes registradas
    for archivo in os.listdir(RUTA_IMAGENES):
        if archivo.endswith(".jpg") or archivo.endswith(".jpeg") or archivo.endswith(".png"):
            ruta_completa = os.path.join(RUTA_IMAGENES, archivo)

            imagen_registrada = face_recognition.load_image_file(ruta_completa)
            encoding_registrado = face_recognition.face_encodings(imagen_registrada)

            if encoding_registrado:
                resultado = face_recognition.compare_faces([encoding_registrado[0]], encoding_desconocido)
                if resultado[0]:
                    # Extraer nombre del archivo (sin extensión)
                    nombre_archivo = os.path.splitext(archivo)[0]

                    # Buscar usuario en DB
                    usuario = db.query(Usuario).filter(Usuario.nombre == nombre_archivo).first()
                    if usuario:
                        return registrar_evento(db, usuario.id, "inicio_sesion")
                    else:
                        raise ValueError(f"Usuario '{nombre_archivo}' no encontrado en la base de datos")

    raise ValueError("Usuario no reconocido")