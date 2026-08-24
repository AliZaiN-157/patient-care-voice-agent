from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Appointment
from app.schemas import AppointmentCreate

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
):
    appointment = Appointment(
        patient_id=payload.patient_id,
        appointment_date=payload.appointment_date,
        appointment_time=payload.appointment_time,
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return {
        "data": {
            "appointment_id": str(appointment.appointment_id),
            "patient_id": str(appointment.patient_id),
            "appointment_date": str(appointment.appointment_date),
            "appointment_time": appointment.appointment_time,
        },
        "error": None,
    }