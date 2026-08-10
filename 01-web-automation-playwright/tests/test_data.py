"""
Centralized test data for KAI Booking automation tests.
All test data is maintained here for easy management.
"""

from datetime import datetime, timedelta


# ============================================================
# Station Codes (Kode Stasiun KAI)
# ============================================================
STATIONS = {
    "PASAR_SENEN": "PSE",
    "GAMBIR": "GMR",
    "BANDUNG": "BD",
    "YOGYAKARTA": "YK",
    "SURABAYA": "SGU",
    "SEMARANG": "SMT",
    "CIREBON": "CN",
    "MALANG": "ML",
    "SOLO": "SLO",
    "PURWOKERTO": "PWT",
}


# ============================================================
# Search Data
# ============================================================
def get_departure_date(days_ahead: int = 7) -> str:
    """Get future departure date in YYYY-MM-DD format."""
    return (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")


VALID_SEARCH = {
    "origin": STATIONS["PASAR_SENEN"],         # PSE
    "destination": STATIONS["BANDUNG"],         # BD
    "departure_date": get_departure_date(7),
    "adults": 1,
    "babies": 0,
}

VALID_SEARCH_ALT = {
    "origin": STATIONS["GAMBIR"],              # GMR
    "destination": STATIONS["YOGYAKARTA"],     # YK
    "departure_date": get_departure_date(10),
    "adults": 2,
    "babies": 0,
}

INVALID_SEARCH = {
    "origin": "XXX",
    "destination": "ZZZ",
    "departure_date": "2099-12-31",
    "adults": 1,
    "babies": 0,
}


# ============================================================
# Login Credentials (override via .env)
# ============================================================
INVALID_CREDENTIALS = {
    "wrong_password": {
        "username": "testuser@example.com",
        "password": "WrongPassword123!",
    },
    "wrong_email": {
        "username": "notregistered@fakemail.com",
        "password": "SomePassword123!",
    },
    "empty": {
        "username": "",
        "password": "",
    },
}


# ============================================================
# Passenger Data
# ============================================================
CONTACT_PERSON = {
    "name": "Bagas Dimas Saputra",
    "phone": "081234567890",
    "email": "bagas.test@example.com",
}

PASSENGER_1 = {
    "name": "BAGAS DIMAS SAPUTRA",
    "id_type": "KTP",
    "id_number": "3171234567890001",
    "phone": "081234567890",
}

PASSENGER_2 = {
    "name": "ANDI PRASETYO",
    "id_type": "KTP",
    "id_number": "3171234567890002",
    "phone": "081298765432",
}

# Empty passenger data for validation testing
EMPTY_CONTACT = {
    "name": "",
    "phone": "",
    "email": "",
}

PARTIAL_CONTACT_NO_NAME = {
    "name": "",
    "phone": "081234567890",
    "email": "test@example.com",
}

PASSENGER_NO_ID = {
    "name": "PASSENGER TEST",
    "id_type": "KTP",
    "id_number": "",
    "phone": "081234567890",
}
