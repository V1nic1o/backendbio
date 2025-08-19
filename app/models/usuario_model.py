from sqlalchemy import Column, Integer, String, LargeBinary
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    codificacion = Column(LargeBinary, nullable=False)
    imagen_path = Column(String, nullable=False)