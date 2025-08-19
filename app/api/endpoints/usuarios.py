from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.usuario_schema import UsuarioOut
from app.services.usuario_service import crear_usuario, obtener_usuarios, verificar_facial
from app.models.usuario_model import Usuario
from app.services.evento_service import registrar_evento

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UsuarioOut)
def registrar(
    nombre: str = Form(...),
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return crear_usuario(db, nombre, imagen)

@router.get("/", response_model=list[UsuarioOut])
def listar(db: Session = Depends(get_db)):
    return obtener_usuarios(db)

@router.post("/login_facial")
def login_facial(
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    usuario = verificar_facial(db, imagen)
    if usuario:
        # ✅ Registrar evento de inicio de sesión si se reconoce al usuario
        registrar_evento(db, usuario.id, "inicio_sesion")
        return {
            "mensaje": "Usuario reconocido",
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Usuario no reconocido")

# ✅ NUEVO: Obtener usuario por ID
@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario