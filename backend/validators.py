import re

email_re = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
phone_re = re.compile(r"^\+?\d{7,15}$")  

def validate_email(email: str) -> bool:
    return bool(email and email_re.match(email))

def validate_phone(phone: str) -> bool:
    return bool(phone and phone_re.match(phone))

def not_empty(*args) -> bool:
    """Retorna True si todos los strings no son vacíos (y existen)."""
    return all(arg is not None and str(arg).strip() != "" for arg in args)
