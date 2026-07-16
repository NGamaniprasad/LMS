"""
System-wide configuration management module.
Defines execution constraints, operational thresholds, and strict data layer endpoints.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

os.makedirs(DATA_DIR, exist_ok=True)

BOOK_FILE = DATA_DIR / "books.json"
STUDENT_FILE = DATA_DIR / "students.json"
ISSUED_FILE = DATA_DIR / "issued_books.json"
USER_FILE = DATA_DIR / "users.json"

DEFAULT_RENEWAL_DAYS = 14
MAX_BORROW_LIMIT = 5
DAILY_FINE_RATE = 2.00

DATE_FORMAT = "%Y-%m-%d"
PHONE_REGEX = r"^\+?[1-9]\d{1,14}$"
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"