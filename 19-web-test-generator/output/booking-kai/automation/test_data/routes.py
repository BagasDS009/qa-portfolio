"""Train route and schedule test data for KAI Booking."""

from datetime import datetime, timedelta


def get_future_day(days_ahead: int = 45) -> str:
    """Get day number N days from now (for datepicker click)."""
    future = datetime.now() + timedelta(days=days_ahead)
    return str(future.day)


def get_months_ahead(days_ahead: int = 45) -> int:
    """Calculate how many months ahead to navigate in datepicker."""
    now = datetime.now()
    future = now + timedelta(days=days_ahead)
    months = (future.year - now.year) * 12 + (future.month - now.month)
    return max(1, months)


# H+45 — far enough to guarantee schedule availability
VALID_ROUTE = {
    "origin": "GMR",       # Gambir, Jakarta
    "destination": "BD",    # Bandung
    "day": get_future_day(45),
    "months_ahead": get_months_ahead(45),
}

VALID_ROUTE_LONG = {
    "origin": "GMR",
    "destination": "SBI",   # Surabaya Pasar Turi
    "day": get_future_day(45),
    "months_ahead": get_months_ahead(45),
}

INVALID_ROUTES = {
    "same_station": {"origin": "GMR", "destination": "GMR", "day": get_future_day(45), "months_ahead": get_months_ahead(45)},
    "empty_origin": {"origin": "", "destination": "BD", "day": get_future_day(45), "months_ahead": get_months_ahead(45)},
    "empty_destination": {"origin": "GMR", "destination": "", "day": get_future_day(45), "months_ahead": get_months_ahead(45)},
}
