from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from .. import models, schemas_filter, schemas, database

router = APIRouter(
    prefix="/api/filters",
    tags=["filters"],
)

@router.post("/", response_model=schemas_filter.Filter)
def create_filter(filter: schemas_filter.FilterCreate, db: Session = Depends(database.get_db)):
    db_filter = models.Filter(**filter.dict())
    db.add(db_filter)
    db.commit()
    db.refresh(db_filter)
    return db_filter

@router.get("/", response_model=List[schemas_filter.Filter])
def read_filters(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    filters = db.query(models.Filter).offset(skip).limit(limit).all()
    return filters

@router.delete("/{filter_id}")
def delete_filter(filter_id: int, db: Session = Depends(database.get_db)):
    db_filter = db.query(models.Filter).filter(models.Filter.id == filter_id).first()
    if db_filter is None:
        raise HTTPException(status_code=404, detail="Filter not found")
    
    db.delete(db_filter)
    db.commit()
    return {"ok": True}

def parse_query(query: str, db: Session):
    base_query = db.query(models.Task)
    
    # Simple parsing logic
    parts = query.lower().split()
    for part in parts:
        if part.startswith("priority:"):
            try:
                p = int(part.split(":")[1])
                base_query = base_query.filter(models.Task.priority == p)
            except:
                pass
        elif part == "due:today":
            today = datetime.now().date()
            base_query = base_query.filter(models.Task.due_date >= today, models.Task.due_date < today + timedelta(days=1))
        elif part == "no:date":
             base_query = base_query.filter(models.Task.due_date == None)
        # Add more logic here as needed (e.g., labels, projects)
    
    return base_query.all()

@router.get("/{filter_id}/tasks", response_model=List[schemas.Task])
def get_filter_tasks(filter_id: int, db: Session = Depends(database.get_db)):
    db_filter = db.query(models.Filter).filter(models.Filter.id == filter_id).first()
    if db_filter is None:
        raise HTTPException(status_code=404, detail="Filter not found")
    
    return parse_query(db_filter.query, db)
