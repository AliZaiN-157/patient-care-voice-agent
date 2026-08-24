from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Appointment, Patient
from app.schemas import AppointmentCreate

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("")
def list_appointments(db: Session = Depends(get_db)):
    appointments = (
        db.query(Appointment, Patient)
        .outerjoin(Patient, Appointment.patient_id == Patient.patient_id)
        .order_by(Appointment.appointment_date, Appointment.appointment_time)
        .all()
    )

    return {
        "data": [
            {
                "appointment_id": str(appt.appointment_id),
                "patient_id": str(appt.patient_id),
                "patient_name": f"{patient.first_name} {patient.last_name}" if patient else "Unknown",
                "appointment_date": str(appt.appointment_date),
                "appointment_time": appt.appointment_time,
                "created_at": appt.created_at.isoformat(),
            }
            for appt, patient in appointments
        ],
        "error": None,
    }


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