from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.patients import router as patient_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(patient_router)


@app.get("/")
def health():
    return {"status": "ok"}