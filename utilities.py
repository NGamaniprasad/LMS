"""
Utility infrastructure component providing foundational validations,
custom decorators, and runtime mutations.
"""

import os
import re
import sys
import logging
from datetime import datetime
from functools import wraps
from typing import Callable, Any
from system_config import PHONE_REGEX, EMAIL_REGEX, DATE_FORMAT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("library_system.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("LibraryCore")


class LibraryException(Exception):
    """Root structural system error handling contract."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class EntityNotFoundError(LibraryException):
    """Raised when looking up an unmapped index target."""


class DuplicateRecordError(LibraryException):
    """Raised when unique natural keys collide inside memory buffers."""


class ValidationFailureError(LibraryException):
    """Raised when parameters break predefined regular validation filters."""


class TransactionBlockedError(LibraryException):
    """Raised when structural boundaries block transactional updates."""


def log_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    """Intercepts and pipes method parameters directly down to logging standard streams."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.debug(f"Entering trace execution context: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Gracefully leaving trace execution context: {func.__name__}")
            return result
        except Exception as error:
            logger.error(f"Bubble capture exception in trace: {func.__name__} -> {str(error)}")
            raise

    return wrapper


class Validator:
    """Static helper validation engine handling structured assertions."""

    @staticmethod
    def validate_phone(phone: str) -> str:
        """Enforces E.164 international structural format checks via standard regex engine."""
        if not re.match(PHONE_REGEX, phone):
            raise ValidationFailureError(f"Phone value '{phone}' breaks system E.164 standardization formats.")
        return phone

    @staticmethod
    def validate_email(email: str) -> str:
        """Verifies operational syntactical state parameters for standard network addresses."""
        if not re.match(EMAIL_REGEX, email):
            raise ValidationFailureError(f"Email domain match parsing failed for value context: '{email}'")
        return email

    @staticmethod
    def validate_date(date_str: str) -> datetime:
        """Ensures incoming date strings perfectly conform to standard timestamp configurations."""
        try:
            return datetime.strptime(date_str, DATE_FORMAT)
        except ValueError:
            raise ValidationFailureError(
                f"Date values must closely track ISO standard format match templates: {DATE_FORMAT}")


class ScreenContext:
    """Manages display presentation clear-buffer calls safely across platform architectures."""

    @staticmethod
    def clear() -> None:
        """Fires terminal clear signals safely based on target kernel identification vectors."""
        os.system("cls" if os.name == "nt" else "clear")