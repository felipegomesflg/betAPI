from operator import and_
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/reviews",
    tags=['Reviews']
)

#####################READ
@router.get("/")
def get_reviews(db: Session = Depends(get_db)):
    data = db.query(models.Review).all()
    return {"data": data}

@router.get("/{id}")
def get_review(id:int, db: Session = Depends(get_db)):
    data = db.query(models.Review).filter(models.Review.id == id).first()
    return {"data": data}
####################CREATE
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):    
    new_data = models.Review(
        **review.dict()
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data}

####################UPDATE
@router.put("/")
def update_review(review: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    data = db.query(models.Review).filter(models.Review.id == review.id)
    old_data = data.first()
    if old_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.update(review.dict(), synchronize_session=False)
    db.commit()
    return {"data": data.first()}

####################DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(id:int, db: Session = Depends(get_db)):
    data = db.query(models.Review).filter(models.Review.id == id)
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

####################CREATE REVIEW COMENT
@router.post("/coment", status_code=status.HTTP_201_CREATED)
def create_review_coment(review: schemas.ReviewComentBaseModel, db: Session = Depends(get_db)):
    new_data = models.ReviewComent(
        **review.dict()
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data}

####################DELETE REVIEW COMENT
@router.delete("/coment/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review_coment(id:int, db: Session = Depends(get_db)):
    data = db.query(models.ReviewComent).filter(models.ReviewComent.id == id)
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

####################CREATE REVIEW COMENT LIKE
@router.post("/comentlike", status_code=status.HTTP_201_CREATED)
def create_review_coment_like(review: schemas.ReviewComentLikeBaseModel, db: Session = Depends(get_db)):
    new_data = models.ReviewComentLike(
        **review.dict()
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data}

####################DELETE REVIEW COMENT LIKE
@router.delete("/comentlike/{userId}/{comentId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review_coment(userId:int, comentId:int, db: Session = Depends(get_db)):
    data = db.query(models.ReviewComentLike).filter(and_(models.ReviewComentLike.userId == userId, models.ReviewComentLike.reviewComentId ==  comentId))
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

####################CREATE REVIEW LIKE
@router.post("/like", status_code=status.HTTP_201_CREATED)
def create_review_like(review: schemas.ReviewLikeBaseModel, db: Session = Depends(get_db)):
    new_data = models.ReviewLike(
        **review.dict()
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"data": new_data}

####################DELETE REVIEW LIKE
@router.delete("/like/{userId}/{reviewId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review_like(userId:int, reviewId:int, db: Session = Depends(get_db)):
    data = db.query(models.ReviewLike).filter(and_(models.ReviewLike.userId == userId, models.ReviewLike.reviewId == reviewId))
    if data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)