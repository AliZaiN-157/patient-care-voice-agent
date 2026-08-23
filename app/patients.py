from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Patient
from app.schemas import PatientCreate

from datetime import datetime
from app.schemas import PatientCreate, PatientUpdate

router = APIRouter(prefix="/patients", tags=["Patients"])

from pydantic import BaseModel

class FindPatientRequest(BaseModel):
    phone_number: str


@router.post("/find")
def find_patient(payload: FindPatientRequest, db: Session = Depends(get_db)):
    patient = (
        db.query(Patient)
        .filter(
            Patient.phone_number == payload.phone_number,
            Patient.deleted_at.is_(None),
        )
        .first()
    )

    return {
        "data": None if not patient else {
            "patient_id": str(patient.patient_id),
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "phone_number": patient.phone_number,
        },
        "error": None,
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    patient = Patient(**payload.model_dump())

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return {
        "data": {
            "patient_id": str(patient.patient_id),
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "phone_number": patient.phone_number,
        },
        "error": None,
    }


@router.get("")
def list_patients(
    last_name: str | None = None,
    date_of_birth: str | None = None,
    phone_number: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Patient).filter(Patient.deleted_at.is_(None))

    if last_name:
        query = query.filter(Patient.last_name.ilike(f"%{last_name}%"))

    if date_of_birth:
        query = query.filter(Patient.date_of_birth == date_of_birth)

    if phone_number:
        query = query.filter(Patient.phone_number == phone_number)

    patients = query.all()

    return {
        "data": [
            {
                "patient_id": str(p.patient_id),
                "first_name": p.first_name,
                "last_name": p.last_name,
                "date_of_birth": str(p.date_of_birth),
                "phone_number": p.phone_number,
            }
            for p in patients
        ],
        "error": None,
    }


@router.get("/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = (
        db.query(Patient)
        .filter(
            Patient.patient_id == patient_id,
            Patient.deleted_at.is_(None),
        )
        .first()
    )

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "data": {
            "patient_id": str(patient.patient_id),
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "date_of_birth": str(patient.date_of_birth),
            "sex": patient.sex,
            "phone_number": patient.phone_number,
            "email": patient.email,
            "address_line_1": patient.address_line_1,
            "address_line_2": patient.address_line_2,
            "city": patient.city,
            "state": patient.state,
            "zip_code": patient.zip_code,
            "insurance_provider": patient.insurance_provider,
            "insurance_member_id": patient.insurance_member_id,
            "preferred_language": patient.preferred_language,
            "emergency_contact_name": patient.emergency_contact_name,
            "emergency_contact_phone": patient.emergency_contact_phone,
        },
        "error": None,
    }

@router.put("/{patient_id}")
def update_patient(
    patient_id: str,
    payload: PatientUpdate,
    db: Session = Depends(get_db),
):
    patient = (
        db.query(Patient)
        .filter(
            Patient.patient_id == patient_id,
            Patient.deleted_at.is_(None),
        )
        .first()
    )

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    return {
        "data": {
            "patient_id": str(patient.patient_id),
            "updated": True,
        },
        "error": None,
    }


@router.delete("/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = (
        db.query(Patient)
        .filter(
            Patient.patient_id == patient_id,
            Patient.deleted_at.is_(None),
        )
        .first()
    )

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient.deleted_at = datetime.utcnow()

    db.commit()

    return {
        "data": {
            "patient_id": str(patient.patient_id),
            "deleted": True,
        },
        "error": None,
    }