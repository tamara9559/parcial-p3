from flask import Flask, request, jsonify
from .repository import init_db
from .services import register_patient, list_all_doctors, schedule_appointment, get_patient_appointments, cancel_appt
from flask import send_from_directory
import os

app = Flask(__name__)



FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.route("/")
def serve_home():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_FOLDER, path)

@app.route("/static/<path:path>")
def serve_static_files(path):
    return send_from_directory(os.path.join(FRONTEND_FOLDER, "static"), path)


init_db()

@app.route("/api/patients", methods=["POST"])
def api_register_patient():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    result = register_patient(name, email, phone)
    if isinstance(result, tuple):
        body, status = result
        return jsonify(body), status
    return jsonify(result)

@app.route("/api/doctors", methods=["GET"])
def api_list_doctors():
    return jsonify(list_all_doctors())

@app.route("/api/appointments", methods=["POST"])
def api_schedule_appointment():
    data = request.get_json() or {}
    doctor_id = data.get("doctor_id")
    patient_id = data.get("patient_id")
    start = data.get("start")  # ISO
    duration = data.get("duration", 30)
    body, status = schedule_appointment(doctor_id, patient_id, start, duration)
    return jsonify(body), status

@app.route("/api/patients/<int:patient_id>/appointments", methods=["GET"])
def api_get_patient_appointments(patient_id):
    return jsonify(get_patient_appointments(patient_id))

@app.route("/api/appointments/<int:appointment_id>", methods=["DELETE"])
def api_cancel_appointment(appointment_id):
    body, status = cancel_appt(appointment_id)
    return jsonify(body), status

if __name__ == "__main__":
    app.run(debug=True, port=5000)
