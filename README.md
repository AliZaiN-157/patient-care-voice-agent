# Voice AI Patient Registration Agent

A voice-based patient registration system built for the **Voice AI Agent Patient Registration**.

The system allows a caller to dial a real U.S. phone number, speak naturally with an AI intake agent, register patient demographic information, update an existing record, and optionally schedule an appointment.

## Architecture

```text
Caller
  ↓
Vapi Voice Agent
  ↓
FastAPI REST API
  ↓
Supabase PostgreSQL

Additional:
- Railway deployment
- Call transcript storage
- Patient dashboard
- Automated API tests
```

## Tech Stack

* **Voice / Telephony:** Vapi
* **Backend:** FastAPI
* **Database:** Supabase PostgreSQL
* **ORM:** SQLAlchemy
* **Validation:** Pydantic
* **Hosting:** Railway
* **Testing:** Pytest

Vapi was selected to minimize telephony, STT, and TTS integration overhead and focus on the conversational logic and backend integration.

## Features

### Patient Registration

The agent collects:

* First name
* Last name
* Date of birth
* Sex
* Phone number
* Street address
* City
* State
* ZIP code

Optional information:

* Email
* Address line 2
* Insurance provider
* Insurance member ID
* Preferred language
* Emergency contact name
* Emergency contact phone

The agent reads the collected information back to the caller before saving it.

### Validation

Server-side validation includes:

* Future date-of-birth prevention
* U.S. phone validation
* Email validation
* U.S. state validation
* ZIP / ZIP+4 validation
* Allowed sex values

Natural voice inputs are normalized where appropriate, for example:

```text
"M" → "Male"
"California" → "CA"
```

### Duplicate Detection

The agent checks for an existing patient using the phone number.

If a patient already exists, the caller is offered the option to update the existing record instead of creating a duplicate.

### Appointment Scheduling

After successful registration, the agent can optionally schedule a mock first appointment.

### Multi-language Support

The assistant can switch to Spanish when the caller speaks Spanish or requests Spanish.

### Call Transcripts

Vapi's end-of-call webhook stores call transcripts in the database for later review.

### Dashboard

Registered patients can be viewed at:

```text
/dashboard
```

## REST API

### List patients

```http
GET /patients
```

Optional filters:

```text
?last_name=
?date_of_birth=
?phone_number=
```

### Get patient

```http
GET /patients/{patient_id}
```

### Create patient

```http
POST /patients
```

### Update patient

```http
PUT /patients/{patient_id}
```

Partial updates are supported.

### Delete patient

```http
DELETE /patients/{patient_id}
```

Deletion is soft-delete based using `deleted_at`.

### Schedule appointment

```http
POST /appointments
```

### Vapi webhook

```http
POST /vapi/webhook
```

Used for end-of-call transcript storage.

## API Response Format

Successful response:

```json
{
  "data": {},
  "error": null
}
```

Error response:

```json
{
  "data": null,
  "error": {}
}
```

## Local Setup

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd patient-care-voice-agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
DATABASE_URL=YOUR_SUPABASE_POSTGRES_CONNECTION_STRING
```

For Supabase, the **Session Pooler connection string** is recommended when running from an IPv4 environment.

Start the API:

```bash
uvicorn app.main:app --reload --port 8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Environment Variables

```env
DATABASE_URL=
```

API keys and credentials are not hardcoded in the repository.

## Deployment

The FastAPI backend is deployed on Railway.

Railway start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Live Demo

**Phone Number**

```text
+1 440-363-8036
```

**API Base URL**

```text
https://patient-care-voice-agent-production.up.railway.app/
```

**Swagger**

```text
https://patient-care-voice-agent-production.up.railway.app/docs
```

**Dashboard**

```text
https://patient-care-voice-agent-production.up.railway.app/dashboard
```

## Voice Agent Behavior

The assistant is instructed to:

* Ask conversational questions rather than use an IVR flow
* Handle information provided out of order
* Handle caller corrections
* Re-prompt invalid fields
* Allow the caller to restart registration
* Offer optional demographic information
* Confirm all collected information before saving
* Detect existing patients
* Gracefully handle backend failures
* Offer appointment scheduling after registration

## Observability

The backend logs patient creation activity and final collected payloads.

Call transcripts are stored through the Vapi end-of-call webhook.

## Known Limitations / Trade-offs

* This is a technical assessment and is **not HIPAA-compliant production software**.
* No real patient data should be used.
* Appointment scheduling uses mock availability rather than a real EHR or scheduling system.
* Duplicate detection currently uses phone number matching.
* Authentication is intentionally omitted to keep the assessment focused on voice AI integration and system design.
* The dashboard is intentionally lightweight.

## Project Structure

```text
app/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── patients.py
├── appointments.py
└── vapi.py

templates/
└── dashboard.html


requirements.txt
.env.example
README.md
```

## Submission

Include:

* Repository URL
* Live Vapi phone number
* Railway API base URL
* Any notes needed for testing

The assessment prioritizes a working end-to-end system, conversational quality, clean architecture, resilience, and clear documentation.