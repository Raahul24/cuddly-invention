from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas_label, database

router = APIRouter(
    prefix="/api/labels",
    tags=["labels"],
)

@router.post("/", response_model=schemas_label.Label)
def create_label(label: schemas_label.LabelCreate, db: Session = Depends(database.get_db)):
    db_label = models.Label(**label.dict())
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

@router.get("/", response_model=List[schemas_label.Label])
def read_labels(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    labels = db.query(models.Label).offset(skip).limit(limit).all()
    return labels

@router.delete("/{label_id}")
def delete_label(label_id: int, db: Session = Depends(database.get_db)):
    db_label = db.query(models.Label).filter(models.Label.id == label_id).first()
    if db_label is None:
        raise HTTPException(status_code=404, detail="Label not found")
    
    db.delete(db_label)
    db.commit()
    return {"ok": True}
