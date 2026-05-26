from fastapi import FastAPI
from dotenv import load_dotenv

from .api.experience import router as experience_router
from .db import create_db_and_tables

load_dotenv()

app = FastAPI(title="Experience Explorer Backend")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(experience_router, prefix="/api")
