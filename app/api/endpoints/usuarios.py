from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.usuario_schema import UsuarioOut
from app.services.usuario_service import crear_usuario, obtener_usuarios, verificar_facial

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
        return {"mensaje": "Usuario reconocido", "usuario": usuario.nombre}
    else:
        raise HTTPException(status_code=401, detail="Usuario no reconocido")