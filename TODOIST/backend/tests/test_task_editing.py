from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database import Base, get_db
import pytest
import os

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_editing.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_editing.db"):
        os.remove("./test_editing.db")

def test_create_and_edit_task(test_db):
    # 1. Create a label first
    res_label = client.post("/api/labels/", json={"name": "Urgent", "color": "red"})
    assert res_label.status_code == 200
    label_id = res_label.json()["id"]

    # 2. Create a task
    response = client.post("/api/tasks/", json={"content": "Original Task"})
    assert response.status_code == 200
    task_id = response.json()["id"]
    
    # 3. Edit the task (content, priority, labels)
    edit_payload = {
        "content": "Updated Task",
        "priority": 4,
        "label_ids": [label_id]
    }
    response = client.put(f"/api/tasks/{task_id}", json=edit_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated Task"
    assert data["priority"] == 4
    assert len(data["labels"]) == 1
    assert data["labels"][0]["id"] == label_id

    # 4. Verify persistence
    response = client.get(f"/api/tasks/{task_id}")
    data = response.json()
    assert data["content"] == "Updated Task"
    assert data["priority"] == 4
    assert data["labels"][0]["name"] == "Urgent"
