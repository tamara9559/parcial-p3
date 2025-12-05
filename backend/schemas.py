from datetime import datetime, timedelta

def parse_iso_datetime(s: str):
    return datetime.fromisoformat(s)

def appointment_input_to_range(start_iso: str, duration_minutes: int = 30):
    start = parse_iso_datetime(start_iso)
    end = start + timedelta(minutes=duration_minutes)
    return start, end
