from blog.token import create_access_token, verify_token
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, models
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(tags=['Auth'])

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid not found')
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect password')
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
