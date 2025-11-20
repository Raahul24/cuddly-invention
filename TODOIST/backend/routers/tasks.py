from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database, utils

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
)

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    db_task = models.Task(**task.dict(exclude={"label_ids"}))
    if task.label_ids:
        labels = db.query(models.Label).filter(models.Label.id.in_(task.label_ids)).all()
        db_task.labels = labels
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    utils.log_activity(db, "created", "task", db_task.id, f"Created task: {db_task.content}")
    return db_task

@router.get("/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    tasks = db.query(models.Task).offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task.dict(exclude_unset=True)
    
    if "label_ids" in update_data:
        label_ids = update_data.pop("label_ids")
        labels = db.query(models.Label).filter(models.Label.id.in_(label_ids)).all()
        db_task.labels = labels

    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    
    if "is_completed" in update_data and update_data["is_completed"]:
        utils.log_activity(db, "completed", "task", db_task.id, f"Completed task: {db_task.content}")
    else:
        utils.log_activity(db, "updated", "task", db_task.id, f"Updated task: {db_task.content}")
        
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    utils.log_activity(db, "deleted", "task", task_id, f"Deleted task: {db_task.content}")
    db.delete(db_task)
    db.commit()
    return {"ok": True}
