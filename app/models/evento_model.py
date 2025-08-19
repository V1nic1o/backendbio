from sqlalchemy import Column, Integer, String, Date, Time, Float, ForeignKey
from app.core.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    tipo = Column(String)
    fecha = Column(Date)
    hora = Column(Time)
    timestamp = Column(Float)