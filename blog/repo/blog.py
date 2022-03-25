from fastapi import HTTPException, status
from blog import models
from sqlalchemy.orm import Session

def get_all_blogs(db: Session):
   
    blogs = db.query(models.Post).all()
    return blogs

def create(db, request):
    
    new_blog = models.Post(title=request.title, body=request.body, author_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return f"added {request.title}, with body: ' {request.body} '"

def get_by_id(db, id):
    
    blog = db.query(models.Post).filter(models.Post.id == id).first()
    if not blog:
        
        raise HTTPException(status_code=404, detail={'message':f'blog with the id {id} is not available'})
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details':f'blog with the id {id} is not available'}
    return blog

def delete(db, id):

    blog = db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit()
    return 'Done'

def update(db, id, request):
    
    blog = db.query(models.Post).filter(models.Post.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    blog.update(request)
    db.commit()