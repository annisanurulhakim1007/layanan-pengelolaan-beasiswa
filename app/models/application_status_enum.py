# app/models/application_status_enum.py
import enum

class ApplicationStatus(str, enum.Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
