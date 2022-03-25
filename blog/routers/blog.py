from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, models, oauth2
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session
from ..repo import blog as blog_repo


router = APIRouter(
    prefix="/blog",
    tags=["Posts"]
)

@router.get('/', response_model=List[schemas.BlogPart])
def get_all_blogs(db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    return blog_repo.get_all_blogs(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    
    return blog_repo.create(db, request)

@router.get('/{id}', status_code=200, response_model=schemas.BlogPart)
def get_by_id(id: int, db: Session = Depends(get_db)):
    
    return blog_repo.get_by_id(db, id)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    
    return blog_repo.delete(db, id)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    
    return blog_repo.update(db, request, id)