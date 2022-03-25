from lib2to3.pytree import Base
from .schemas import *
from .models import *
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import blog, user, login
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI


Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(login.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost",
    "https://localhost:8000",
    "http://localhost",
    "https://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)