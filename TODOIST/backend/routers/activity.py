from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas_activity, database

router = APIRouter(
    prefix="/api/activity",
    tags=["activity"],
)

@router.get("/", response_model=List[schemas_activity.ActivityLog])
def read_activity_logs(skip: int = 0, limit: int = 50, db: Session = Depends(database.get_db)):
    logs = db.query(models.ActivityLog).order_by(models.ActivityLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs
