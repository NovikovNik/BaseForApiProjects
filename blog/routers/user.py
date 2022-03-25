from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from .. import models, schemas, oauth2
from ..hashing import Hash
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.GetUser)
def create_user(request: schemas.User, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    '''Only HeadAdmin (created while init new database) can create other users!'''
    user = models.User(name=request.name, password=Hash.bcrypt(
        request.password), email=request.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/', response_model=List[schemas.GetUser])
def get_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user


@router.get('/{id}', response_model=schemas.GetUser)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


@router.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
