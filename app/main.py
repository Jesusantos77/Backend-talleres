from fastapi import FastAPI
from app.db.session import engine
from app.models.usuarios import Base
from app.routers.usuarios import router
from app.routers.vehiculos import router
from app.routers.solicitudes import router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

##origins = [
 ##   "http://localhost:3000",
  #  "http://127.0.0.1:3000",
#]

ALLOWED_ORIGINS=os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)