from datetime import timedelta
from .repository import (
    create_patient, get_patient_by_email, list_doctors, create_appointment,
    get_appointments_for_doctor_between, list_appointments_for_patient, cancel_appointment
)
from .validators import validate_email, validate_phone, not_empty
from sqlalchemy import not_
from .models import Appointment

def register_patient(name: str, email: str, phone: str):
    if not not_empty(name, email, phone):
        return {"error": "Campos obligatorios faltantes"}, 400
    if not validate_email(email):
        return {"error": "Email inválido"}, 400
    if not validate_phone(phone):
        return {"error": "Teléfono inválido"}, 400
    existing = get_patient_by_email(email)
    if existing:
        return {"error": "Email ya registrado"}, 400
    p = create_patient(name=name, email=email, phone=phone)
    return p.to_dict(), 201

def list_all_doctors():
    doctors = list_doctors()
    return [d.to_dict() for d in doctors]

def schedule_appointment(doctor_id: int, patient_id: int, start_iso: str, duration_minutes: int = 30):
    from datetime import datetime
    start = datetime.fromisoformat(start_iso)
    end = start + timedelta(minutes=duration_minutes)

    overlapping = get_appointments_for_doctor_between(doctor_id, start, end)
    if overlapping:
        return {"error": "El doctor ya tiene una cita en ese horario"}, 409

    appt = create_appointment(doctor_id=doctor_id, patient_id=patient_id, start_dt=start, end_dt=end)
    return appt.to_dict(), 201

def get_patient_appointments(patient_id: int):
    appts = list_appointments_for_patient(patient_id)
    return [a.to_dict() for a in appts]

def cancel_appt(appointment_id: int):
    appt = cancel_appointment(appointment_id)
    if not appt:
        return {"error": "Cita no encontrada"}, 404
    return appt, 200
    
