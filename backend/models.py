from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    phone = Column(String(30), nullable=False)

    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "phone": self.phone}


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    specialty = Column(String(120), nullable=True)

    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "specialty": self.specialty}


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    start = Column(DateTime, nullable=False)  # start datetime
    end = Column(DateTime, nullable=False)    # end datetime
    status = Column(String(30), nullable=False, default="scheduled")  # scheduled | canceled

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")

    __table_args__ = (
        UniqueConstraint("doctor_id", "start", name="uix_doctor_start"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "status": self.status
        }
