from lib2to3.pytree import Base
from pyexpat import model
from turtle import title
from fastapi import Depends, FastAPI, status, Response, HTTPException
from pydantic import BaseModel
from .schemas import *
from .models import *
from .database import engine, session
from sqlalchemy.orm import Session
from . import models
from blog import schemas
from typing import List
from .hashing import Hash
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(engine)

def get_db():
    
    db = session()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

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

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=["Posts"])
def create(request: Blog, db: Session = Depends(get_db)):
    
    new_blog = models.Post(title=request.title, body=request.body, author_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return f"added {request.title}, with body: ' {request.body} '"

@app.get('/blog', response_model=List[schemas.BlogPart], tags=["Posts"])
def get_all_blogs(db: Session = Depends(get_db)):
    
    blogs = db.query(models.Post).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.BlogPart, tags=["Posts"])
def get_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    
    blog = db.query(models.Post).filter(models.Post.id == id).first()
    if not blog:
        
        raise HTTPException(status_code=404, detail={'message':f'blog with the id {id} is not available'})
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details':f'blog with the id {id} is not available'}
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Posts"])
def delete(id, db: Session = Depends(get_db)):
    
    blog = db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Posts"])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    
    blog = db.query(models.Post).filter(models.Post.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    blog.update(request)
    db.commit()
    return 'updated'

@app.post('/user', status_code=status.HTTP_201_CREATED, tags=["User"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    user = models.User(name=request.name, password=Hash.bcrypt(request.password), email=request.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get('/user', response_model = List[schemas.GetUser], tags=["User"])
def create_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user

@app.get('/user/{id}', response_model = schemas.GetUser, tags=["User"])
def create_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user