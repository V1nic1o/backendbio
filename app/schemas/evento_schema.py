from pydantic import BaseModel
from datetime import date, time

class EventoBase(BaseModel):
    usuario_id: int
    tipo: str

class EventoOut(EventoBase):
    id: int
    fecha: date
    hora: time
    timestamp: float

    class Config:
        orm_mode = True