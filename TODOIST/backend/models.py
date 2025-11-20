from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    color = Column(String, default="grey")
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    priority = Column(Integer, default=1) # 1=Normal, 4=Urgent
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    project = relationship("Project", back_populates="tasks")
    labels = relationship("Label", secondary="task_labels", back_populates="tasks")
    reminders = relationship("Reminder", back_populates="task")

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    color = Column(String, default="grey")

    tasks = relationship("Task", secondary="task_labels", back_populates="labels")

class TaskLabel(Base):
    __tablename__ = "task_labels"

    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    label_id = Column(Integer, ForeignKey("labels.id"), primary_key=True)

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    remind_at = Column(DateTime(timezone=True))
    is_sent = Column(Boolean, default=False)

    task = relationship("Task", back_populates="reminders")
    
    # Enhanced Reminder Fields
    type = Column(String, default="absolute") # absolute, relative, location
    relative_offset_minutes = Column(Integer, nullable=True) # e.g., 10, 60
    location_name = Column(String, nullable=True) # e.g., "Home", "Work"
    location_trigger = Column(String, nullable=True) # enter, leave
    latitude = Column(String, nullable=True) # Stored as string for simplicity or Float
    longitude = Column(String, nullable=True)

class Filter(Base):
    __tablename__ = "filters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    query = Column(String)
    color = Column(String, default="grey")
    is_favorite = Column(Boolean, default=False)

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String) # created, updated, completed, deleted
    entity_type = Column(String) # task, project
    entity_id = Column(Integer)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

