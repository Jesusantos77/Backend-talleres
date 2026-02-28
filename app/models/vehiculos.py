from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Vehiculo(Base):
    __tablename__="vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    año = Column(String(100), nullable=False)
    color = Column(String(100), nullable=False)
    placa = Column(String(100), nullable=False)
    imagen = Column(String(150), nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    user_id =Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )


