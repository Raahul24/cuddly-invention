from pydantic import BaseModel
from datetime import datetime

class ReminderBase(BaseModel):
    task_id: int
    remind_at: datetime | None = None
    is_sent: bool = False
    type: str = "absolute"
    relative_offset_minutes: int | None = None
    location_name: str | None = None
    location_trigger: str | None = None
    latitude: float | None = None
    longitude: float | None = None

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int

    class Config:
        orm_mode = True
