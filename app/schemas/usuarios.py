from pydantic import BaseModel, Field
from typing import Optional

class usuarioCreate (BaseModel):
    nombre:str
    apellido:str
    correo:str
    password:str 
    telefono:Optional[str] = None


class usuarioResponse(BaseModel):
    id:int
    nombre:str
    apellido:str
    class Config:
        from_attributes=True

class usuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido : Optional[str] = None
    correo :Optional[str] = None
    password:Optional[str] = None
    telefono:Optional[str] = None


class TokenResponse(BaseModel):
    access_token:str
    token_type:str
