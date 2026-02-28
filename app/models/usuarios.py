from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class Usuario(Base):
    __tablename__="usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    apellido = Column(String(150), nullable=False)
    correo =Column(String(150), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    fecha_creacion=Column(TIMESTAMP, server_default=func.now())

    

