from pydantic import BaseModel

class SolicitudCreate(BaseModel):
    descripcion:str
    vehiculo_id :int 