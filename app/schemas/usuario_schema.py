from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str

class UsuarioCreate(UsuarioBase):
    codificacion: bytes
    imagen_path: str

class UsuarioOut(UsuarioBase):
    id: int
    imagen_path: str

    class Config:
        orm_mode = True