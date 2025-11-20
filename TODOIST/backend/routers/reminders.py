from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas_reminder, database

router = APIRouter(
    prefix="/api/reminders",
    tags=["reminders"],
)

from datetime import timedelta

@router.post("/", response_model=schemas_reminder.Reminder)
def create_reminder(reminder: schemas_reminder.ReminderCreate, db: Session = Depends(database.get_db)):
    reminder_data = reminder.dict()
    
    # Logic for relative reminders
    if reminder.type == "relative" and reminder.relative_offset_minutes:
        task = db.query(models.Task).filter(models.Task.id == reminder.task_id).first()
        if task and task.due_date:
            reminder_data['remind_at'] = task.due_date - timedelta(minutes=reminder.relative_offset_minutes)
            
    db_reminder = models.Reminder(**reminder_data)
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: int, db: Session = Depends(database.get_db)):
    db_reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()
    if db_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    db.delete(db_reminder)
    db.commit()
    return {"ok": True}
