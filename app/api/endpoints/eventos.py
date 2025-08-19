from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.evento_service import registrar_evento_con_rostro, obtener_eventos
from app.schemas.evento_schema import EventoOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EventoOut)
async def registrar(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        evento = await registrar_evento_con_rostro(db, file)
        return evento
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al procesar imagen o rostro")

@router.get("/", response_model=list[EventoOut])
def listar(db: Session = Depends(get_db)):
    return obtener_eventos(db)