from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ActivityLogBase(BaseModel):
    event_type: str
    entity_type: str
    entity_id: int
    description: str

class ActivityLogCreate(ActivityLogBase):
    pass

class ActivityLog(ActivityLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
