from lib2to3.pytree import Base
from turtle import title
from fastapi import Depends, FastAPI, status, Response, HTTPException
from pydantic import BaseModel
from .schemas import *
from .models import *
from .database import engine, session
from sqlalchemy.orm import Session
from . import models

Base.metadata.create_all(engine)

def get_db():
    
    db = session()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: Blog, db: Session = Depends(get_db)):
    
    new_blog = models.Post(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return f"added {request.title}, with body: ' {request.body} '"

@app.get('/blog')
def get_all_blogs(db: Session = Depends(get_db)):
    
    blogs = db.query(models.Post).all()
    return blogs

@app.get('/blog/{id}', status_code=200)
def get_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    
    blog = db.query(models.Post).filter(models.Post.id == id).first()
    if not blog:
        
        raise HTTPException(status_code=404, detail={'message':f'blog with the id {id} is not available'})
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details':f'blog with the id {id} is not available'}
    return blog