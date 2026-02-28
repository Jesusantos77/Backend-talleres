from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.usuarios import usuarioCreate, usuarioResponse, usuarioUpdate, TokenResponse
from app.models.usuarios import Usuario
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token, hash_password, get_current_user
from datetime import timedelta

router = APIRouter()

@router.get(
    "/me"
)

def obtener_usuario_actual(
    current_user:Usuario=Depends(get_current_user)
):
    return current_user


@router.post(
    "/usuarios/",
    response_model= usuarioResponse,
    status_code=201
)

def crear_usuarios(
    user:usuarioCreate,
    db:Session=Depends(get_db)
):
    
    existe = db.query(Usuario).filter(
        Usuario.correo==user.correo
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Usuario registrado"
        )
    
    nuevo_usuario= Usuario(
        nombre = user.nombre,
        apellido = user.apellido,
        correo = user.correo,
        telefono= user.telefono,
        password_hash =hash_password(user.password)

    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario

@router.get(
    "/usuarios/",
    response_model=list[usuarioResponse]
)

def listar_usuarios(
    db:Session=Depends(get_db),
):
    return db.query(Usuario).all()

@router.delete(
    "/usuarios/{id}",
    status_code=204
)

def eliminar_usuario(
    id:int,
    db:Session=Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id==id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()


@router.put(
    "/usuarios/",
    response_model=usuarioResponse,
    status_code=200
)

def actualizar_usuario(
    user: usuarioUpdate,
    db:Session=Depends(get_db),
    current_user:Usuario=Depends(get_current_user)
):
    uptdate_data = user.dict(exclude_unset=True)

    for key, value in uptdate_data.items():

        if key == "password":
            value = hash_password(value)

        setattr(current_user, key, value)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.post(
    "/login",
    response_model=TokenResponse
)

def login(
    form_data:OAuth2PasswordRequestForm =Depends(),
    db:Session =Depends(get_db)
):
    user = db.query(Usuario).filter(
        Usuario.correo==form_data.username
    ).first()


    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    token = create_access_token(
        data={"sub":str(user.id)},
        expires_delta=timedelta(minutes=60)
    )

    return{
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/perfil/")

def obtener_perfil(
    current_user:Usuario=Depends(get_current_user)
):
    return current_user