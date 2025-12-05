import pytest
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta

API_BASE = "http://localhost:5000/api"

def create_patient_api(name, email, phone):
    r = requests.post(f"{API_BASE}/patients", json={"name": name, "email": email, "phone": phone})
    return r

def list_doctors_api():
    r = requests.get(f"{API_BASE}/doctors")
    return r.json()

def schedule_appointment_api(doctor_id, patient_id, start_iso, duration=30):
    r = requests.post(f"{API_BASE}/appointments", json={
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "start": start_iso,
        "duration": duration
    })
    return r

def get_patient_appointments_api(patient_id):
    r = requests.get(f"{API_BASE}/patients/{patient_id}/appointments")
    return r

def cancel_appointment_api(app_id):
    r = requests.delete(f"{API_BASE}/appointments/{app_id}")
    return r

def test_full_flow_register_and_schedule_and_cancel(browser):
    name = "Test User"
    email = "testuser@example.com"
    phone = "+573001112233"
    r = create_patient_api(name, email, phone)
    assert r.status_code == 201
    patient = r.json()
    patient_id = patient["id"]

    doctors = list_doctors_api()
    doctor_id = doctors[0]["id"]

    start_dt = (datetime.now() + timedelta(hours=1)).replace(second=0, microsecond=0)
    start_iso = start_dt.isoformat()
    resp = schedule_appointment_api(doctor_id, patient_id, start_iso)
    assert resp.status_code == 201
    appt = resp.json()
    appt_id = appt["id"]

    r2 = get_patient_appointments_api(patient_id)
    assert r2.status_code == 200
    appts = r2.json()
    assert any(a["id"] == appt_id for a in appts)

    rc = cancel_appointment_api(appt_id)
    assert rc.status_code == 200
    data = rc.json()
    assert data["status"] == "canceled"

def test_invalid_email_and_empty_fields():
    r = create_patient_api("", "bad-email", "")
    assert r.status_code == 400

def test_double_booking_conflict():
    p1 = create_patient_api("Alice", "alice@example.com", "+573001112234").json()
    p2 = create_patient_api("Bob", "bob@example.com", "+573001112235").json()
    doctors = list_doctors_api()
    doctor_id = doctors[0]["id"]

    start_dt = (datetime.now() + timedelta(hours=2)).replace(second=0, microsecond=0)
    start_iso = start_dt.isoformat()

    r1 = schedule_appointment_api(doctor_id, p1["id"], start_iso)
    assert r1.status_code == 201

    r2 = schedule_appointment_api(doctor_id, p2["id"], start_iso)
    assert r2.status_code == 409
