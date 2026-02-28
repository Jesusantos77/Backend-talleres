from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.vehiculos import vehiculoUpdate, vehiculoCreate, vehiculoResponse
from app.models.vehiculos import Vehiculo
from app.models.usuarios import Usuario
from app.routers.usuarios import router
from app.core.security import get_current_user

@router.post(
    "/vehiculos/",
    response_model= vehiculoResponse,
    status_code=201    
)

def crear_vehiculo(
    vehiculo: vehiculoCreate,
    db:Session=Depends(get_db),
    current_user:Usuario=Depends(get_current_user)
):
    existe = db.query(Vehiculo).filter(
        Vehiculo.placa == vehiculo.placa, 
        Vehiculo.user_id== current_user.id).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Vehiculo ya registrado"
        )

    nuevo_vehiculo=Vehiculo(
        user_id = current_user.id,
        marca = vehiculo.marca,
        modelo = vehiculo. modelo,
        año = vehiculo.año,
        color= vehiculo.color,
        placa= vehiculo.placa,
    )

    db.add(nuevo_vehiculo)
    db.commit()
    db.refresh(nuevo_vehiculo)

    return nuevo_vehiculo


@router.get(
    "/vehiculos",
    response_model=list[vehiculoResponse]
)

def listar_vehiculos(
    db: Session = Depends(get_db),
    current_user:Usuario=Depends(get_current_user)
):
    lista = db.query(Vehiculo).filter(
        Vehiculo.user_id== current_user.id
    ).all()
    return lista

@router.put(
    "/vehiculos/{id}",
    response_model=vehiculoResponse,
    status_code=200
)

def actualizar_vehiculo(
    id: int,
    vehiculo: vehiculoUpdate,
    db:Session=Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    vehiculo_existente=db.query(Vehiculo).filter(Vehiculo.user_id==current_user.id).first()

    if not vehiculo_existente:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    for key, value in vehiculo.dict(exclude_unset=True).items():
        setattr(vehiculo_existente, key, value)

    db.commit()
    db.refresh(vehiculo_existente)
    return vehiculo_existente

@router.delete(
    "/vehiculos/{id}",
    status_code=204
)

def eliminar_vehiculo(
    id:int,
    db:Session=Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.user_id == current_user.id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    
    db.delete(vehiculo)
    db.commit()

@router.get(
    "/vehiculos/{id}",
)

def obtenerVehiculo(
    id:int,
    db:Session=Depends(get_db),
    current_user:Usuario=Depends(get_current_user)
):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id==id, Vehiculo.user_id==current_user.id).first()

    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

    return vehiculo



