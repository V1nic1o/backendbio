from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class EventoBase(BaseModel):
    usuario_id: int
    tipo: str

class EventoOut(BaseModel):
    id: int
    usuario_id: int
    tipo: str
    fecha: date
    hora: time
    timestamp: float
    nombre_usuario: Optional[str]  # 🔹 Se marca como opcional

    class Config:
        orm_mode = True