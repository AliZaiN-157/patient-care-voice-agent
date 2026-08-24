from fastapi import FastAPI

from app.database import Base, engine, get_db
from app import models
from app.patients import router as patient_router

from fastapi import Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse

from sqlalchemy.orm import Session
from app.models import CallLog

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(patient_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "data": None,
            "error": exc.errors(),
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "data": None,
            "error": "Internal server error",
        },
    )

@app.post("/vapi/webhook")
async def vapi_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    payload = await request.json()

    message = payload.get("message", {})
    call = message.get("call", {})

    artifact = message.get("artifact", {})
    transcript = artifact.get("transcript")
    summary = message.get("summary")

    if transcript or summary:
        log = CallLog(
            vapi_call_id=call.get("id"),
            transcript=transcript,
            summary=summary,
        )

        db.add(log)
        db.commit()

    return {"data": {"received": True}, "error": None}

@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/dashboard")
def dashboard():
    return FileResponse("templates/dashboard.html")