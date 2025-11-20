from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .routers import tasks, projects, reminders, labels, filters, activity

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todoist Clone API", version="0.1.0")

# Mount static files
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Templates
templates = Jinja2Templates(directory="backend/templates")

# Include Routers
app.include_router(tasks.router)
app.include_router(projects.router)
app.include_router(reminders.router)
app.include_router(labels.router)
app.include_router(filters.router)
app.include_router(activity.router)

# CORS configuration (still good to have)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Todoist Clone"})

