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
    "CIREBON_PRUJAKAN": "CNP",
    "MALANG": "ML",
    "SOLO": "SLO",
    "PURWOKERTO": "PWT",
}


# ============================================================
# Search Data
# ============================================================
def get_departure_date(days_ahead: int = 7) -> str:
    """
    Get future departure day number as string.
    Used by set_departure_date() which clicks the day in datepicker.
    Returns: Day number string (e.g., "17", "25")
    """
    target = datetime.now() + timedelta(days=days_ahead)
    return str(target.day)


def get_departure_date_parts(days_ahead: int = 7) -> dict:
    """Get departure date broken into parts (for manual datepicker control)."""
    target = datetime.now() + timedelta(days=days_ahead)
    return {
        "day": str(target.day),
        "month": target.month,
        "year": target.year,
    }


def get_departure_id(tgl: str) -> str:
    """
    Generate departure ID in format YYYYMMDD (next month + tgl).
    Used for XPath: //a[@onclick="document.getElementById('data-20260924').submit()..."]
    """
    from datetime import datetime
    now = datetime.now()
    # Next month (since datepicker clicks next month)
    month = now.month + 1
    year = now.year
    if month > 12:
        month = 1
        year += 1
    return f"{year}{month:02d}{int(tgl):02d}"


VALID_SEARCH = {
    "origin": STATIONS["PASAR_SENEN"],         # PSE
    "destination": STATIONS["BANDUNG"],         # BD
    "tgl": "24",                               # Tanggal 24
    "departure_id": get_departure_id("24"),    # e.g., "20260924"
    "train_name": "Cikuray",   # Nama kereta yang dipilih
    "adults": 1,
    "babies": 0,
}

VALID_SEARCH_ALT = {
    "origin": STATIONS["GAMBIR"],              # GMR
    "destination": STATIONS["YOGYAKARTA"],     # YK
    "tgl": "15",                               # Tanggal 15
    "departure_id": get_departure_id("15"),    # e.g., "20260915"
    "adults": 2,
    "babies": 0,
}

INVALID_SEARCH = {
    "origin": "XXX",
    "destination": "ZZZ",
    "tgl": "31",
    "adults": 1,
    "babies": 0,
}

VALID_SEARCH_NOT_FOUND = {
    "origin": STATIONS["GAMBIR"],         # PSE (valid station)
    "destination": STATIONS["CIREBON_PRUJAKAN"],         # BD (valid station)
    "tgl": "15",                               # Tanggal 15 (pasti ada di calendar)
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
