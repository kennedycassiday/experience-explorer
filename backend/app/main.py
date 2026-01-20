from .models import User, Experience
from .db import create_db_and_tables, engine
from fastapi import FastAPI
from sqlmodel import Session

app = FastAPI(title="Experience Explorer Backend")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/user")
def create_user(user: User):
    session = Session(engine)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/experience")
def create_experience(experience: Experience):
    session = Session(engine)
    session.add(experience)
    session.commit()
    session.refresh(experience)
    return experience
