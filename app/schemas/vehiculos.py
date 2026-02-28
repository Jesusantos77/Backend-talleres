from pydantic import BaseModel, Field
from typing import Optional

class vehiculoCreate(BaseModel):
    marca:str
    modelo:str
    año:str
    color:str
    placa:str
    imagen:Optional[str] = None

class vehiculoResponse(BaseModel):
    id:int
    marca:str
    modelo:str
    año:str
    color:str
    placa:str
    imagen:Optional[str] = None

class vehiculoUpdate(BaseModel):
    marca:Optional[str] = None
    modelo:Optional[str] = None
    año:Optional[str] = None
    color:Optional[str] = None
    placa:Optional[str] = None
    imagen:Optional[str] = None