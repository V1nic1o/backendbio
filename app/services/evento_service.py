import os
import face_recognition
from fastapi import UploadFile
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from app.models.evento_model import Evento
from app.models.usuario_model import Usuario
import io

# Ruta a las imágenes registradas
RUTA_IMAGENES = "imagenes_rostros"

def registrar_evento(db: Session, usuario_id: int, tipo: str):
    ahora = datetime.now()
    nuevo_evento = Evento(
        usuario_id=usuario_id,
        tipo=tipo,
        fecha=ahora.date(),
        hora=ahora.time(),
        timestamp=float(ahora.timestamp())
    )
    db.add(nuevo_evento)
    db.commit()
    db.refresh(nuevo_evento)
    return nuevo_evento

def obtener_eventos(db: Session):
    # ✅ Incluir la relación con el usuario para acceder a su nombre
    eventos = db.query(Evento).options(joinedload(Evento.usuario)).all()
    return eventos

async def registrar_evento_con_rostro(db: Session, file: UploadFile):
    contenido = await file.read()
    buffer = io.BytesIO(contenido)

    imagen_desconocida = face_recognition.load_image_file(buffer)
    rostros_desconocidos = face_recognition.face_encodings(imagen_desconocida)

    if not rostros_desconocidos:
        raise ValueError("No se detectó ningún rostro en la imagen")

    encoding_desconocido = rostros_desconocidos[0]

    for archivo in os.listdir(RUTA_IMAGENES):
        if archivo.lower().endswith((".jpg", ".jpeg", ".png")):
            ruta_completa = os.path.join(RUTA_IMAGENES, archivo)

            imagen_registrada = face_recognition.load_image_file(ruta_completa)
            encoding_registrado = face_recognition.face_encodings(imagen_registrada)

            if encoding_registrado:
                resultado = face_recognition.compare_faces([encoding_registrado[0]], encoding_desconocido)
                if resultado[0]:
                    # ✅ Buscar por ruta completa (como ya se guarda)
                    usuario = db.query(Usuario).filter(Usuario.imagen_path == ruta_completa).first()
                    if usuario:
                        return registrar_evento(db, usuario.id, "inicio_sesion")
                    else:
                        raise ValueError(f"Usuario con imagen '{archivo}' no encontrado en la base de datos")

    raise ValueError("Usuario no reconocido")