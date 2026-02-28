from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class SolicitudServicio(Base):
    __tablename__="solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    usuario_id=Column(Integer, ForeignKey("usuarios.id"))
    vehiculo_id=Column(Integer, ForeignKey("vehiculos.id"))
    estado = Column(String, default="pendiente")
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())