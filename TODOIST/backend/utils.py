from sqlalchemy.orm import Session
from . import models

def log_activity(db: Session, event_type: str, entity_type: str, entity_id: int, description: str):
    activity = models.ActivityLog(
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description
    )
    db.add(activity)
    db.commit()
