from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
import re


VALID_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
    "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
}


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    sex: str
    phone_number: str

    email: Optional[EmailStr] = None

    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str
    zip_code: str

    insurance_provider: Optional[str] = None
    insurance_member_id: Optional[str] = None

    preferred_language: Optional[str] = "English"

    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

    @field_validator(
    "email",
    "address_line_2",
    "insurance_provider",
    "insurance_member_id",
    "preferred_language",
    "emergency_contact_name",
    "emergency_contact_phone",
    mode="before"
    )
    @classmethod
    def empty_to_none(cls, value):
        if value == "":
            return None
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, value):
        if value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return value

    @field_validator("sex", mode="before")
    @classmethod
    def validate_sex(cls, value):
        value = str(value).strip().lower()

        mapping = {
            "m": "Male",
            "male": "Male",
            "f": "Female",
            "female": "Female",
            "other": "Other",
            "decline": "Decline to Answer",
            "decline to answer": "Decline to Answer",
            "prefer not to say": "Decline to Answer",
        }

        if value not in mapping:
            raise ValueError("Invalid sex value")

        return mapping[value]

    @field_validator("phone_number", "emergency_contact_phone")
    @classmethod
    def validate_phone(cls, value):
        if value is None:
            return value

        digits = re.sub(r"\D", "", value)

        if len(digits) != 10:
            raise ValueError("Phone number must contain 10 digits")

        return digits

    @field_validator("state")
    @classmethod
    def validate_state(cls, value):
        value = value.upper()
        if value not in VALID_STATES:
            raise ValueError("Invalid U.S. state abbreviation")
        return value

    @field_validator("zip_code")
    @classmethod
    def validate_zip(cls, value):
        if not re.fullmatch(r"\d{5}(-\d{4})?", value):
            raise ValueError("Invalid ZIP code")
        return value

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    sex: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_member_id: Optional[str] = None
    preferred_language: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class AppointmentCreate(BaseModel):
    patient_id: str
    appointment_date: date
    appointment_time: str