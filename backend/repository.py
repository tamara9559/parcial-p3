from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_, not_, inspect
from .config import DATABASE_URL
from .models import Base, Patient, Doctor, Appointment
from datetime import datetime

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        if session.query(Doctor).count() == 0:
            session.add_all([
                Doctor(name="Dr. Ana Pérez", specialty="Pediatría"),
                Doctor(name="Dr. Juan Gómez", specialty="Medicina General"),
                Doctor(name="Dra. Carla Ruiz", specialty="Dermatología")
            ])
            session.commit()
    finally:
        session.close()


def create_patient(name: str, email: str, phone: str):
    session = SessionLocal()
    try:
        p = Patient(name=name, email=email, phone=phone)
        session.add(p)
        session.commit()
        session.refresh(p)
        return p
    finally:
        session.close()

def get_patient_by_email(email: str):
    session = SessionLocal()
    try:
        return session.query(Patient).filter(Patient.email == email).first()
    finally:
        session.close()

def get_patient(patient_id: int):
    session = SessionLocal()
    try:
        return session.query(Patient).get(patient_id)
    finally:
        session.close()

def list_doctors():
    session = SessionLocal()
    try:
        return session.query(Doctor).all()
    finally:
        session.close()

def create_appointment(doctor_id: int, patient_id: int, start_dt, end_dt):
    session = SessionLocal()
    try:
        appt = Appointment(doctor_id=doctor_id, patient_id=patient_id, start=start_dt, end=end_dt, status="scheduled")
        session.add(appt)
        session.commit()
        session.refresh(appt)
        return appt
    finally:
        session.close()

def get_appointments_for_doctor_between(doctor_id: int, start_dt, end_dt):
    session = SessionLocal()
    try:
        return session.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status == "scheduled",
            not_(
                (Appointment.end <= start_dt) | (Appointment.start >= end_dt)
            )
        ).all()
    finally:
        session.close()

def list_appointments_for_patient(patient_id: int):
    session = SessionLocal()
    try:
        return session.query(Appointment).filter(Appointment.patient_id == patient_id).all()
    finally:
        session.close()

def cancel_appointment(appointment_id: int):
    session = SessionLocal()
    try:
        appt = session.query(Appointment).get(appointment_id)
        if not appt:
            return None

        appt.status = "canceled"
        session.commit()

        # convertir antes de cerrar sesión
        result = {
            "id": appt.id,
            "doctor_id": appt.doctor_id,
            "patient_id": appt.patient_id,
            "start": appt.start.isoformat(),
            "end": appt.end.isoformat(),
            "status": appt.status
        }

        return result

    finally:
        session.close()



def reset_all():
    session = SessionLocal()
    session.query(Appointment).delete()
    session.query(Patient).delete()
    session.commit()
    session.close()
    engine.dispose()



def close_all_connections():
    engine.dispose()
