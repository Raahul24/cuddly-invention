from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .schemas_reminder import Reminder
from .schemas_label import Label
from .schemas_filter import Filter
from .schemas_activity import ActivityLog

class ProjectBase(BaseModel):
    name: str
    color: str = "grey"
    is_favorite: bool = False

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    content: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: int = 1
    project_id: Optional[int] = None

class TaskCreate(TaskBase):
    label_ids: List[int] = []

class TaskUpdate(TaskBase):
    is_completed: Optional[bool] = None
    label_ids: Optional[List[int]] = None

class Task(TaskBase):
    id: int
    is_completed: bool
    created_at: datetime
    reminders: List[Reminder] = []
    labels: List[Label] = []

    class Config:
        orm_mode = True
