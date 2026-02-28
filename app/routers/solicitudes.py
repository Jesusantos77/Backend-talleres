from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.vehiculos import vehiculoUpdate, vehiculoCreate, vehiculoResponse
from app.models.vehiculos import Vehiculo
from app.models.usuarios import Usuario
from app.models.solicitudes import SolicitudServicio
from app.schemas.solicitudes import SolicitudCreate
from app.routers.usuarios import router
from app.core.security import get_current_user

@router.post(
    "/solicitudes/"
)

def crear_solicitud(
    solicitud:SolicitudCreate,
    db:Session=Depends(get_db),
    current_user:Usuario=Depends(get_current_user)
):
    nueva_solicitud = SolicitudServicio (
        descripcion = solicitud.descripcion,
        estado="pendiente",
        vehiculo_id= solicitud.vehiculo_id,
        usuario_id=current_user.id
    )

    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)

    return nueva_solicitud

@router.put(
    "/solicitudes/{id}"
)

def finalizarSolicitud(
    id:int,
    db:Session=Depends(get_db),
    current_user:Usuario=Depends(get_current_user)
):
    solicitud= db.query(SolicitudServicio).filter(SolicitudServicio.id==id, SolicitudServicio.usuario_id==current_user.id).first()

    if  not solicitud:
        raise HTTPException(status_code=404,detail="Solicitud no encontrada")
    
    solicitud.estado="finalizada"
    db.commit()
    db.refresh(solicitud)

    return{"mensaje":"Solicitud finalizada correctamente"}

