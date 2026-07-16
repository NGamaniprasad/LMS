"""
Provides infrastructure handling roles, secure verification steps,
and application session controls.
"""

import hashlib
from typing import Dict, Any, Optional
from models import Profile
from file_handler import FileStoreManager
from system_config import USER_FILE
from utilities import log_execution, DuplicateRecordError


class OperatorUser(Profile):
    """Models internal operational staff parameters."""

    def __init__(self, uid: str, name: str, email: str, secret_hash: str) -> None:
        super().__init__(uid, name, email)
        self.secret_hash = secret_hash


class SessionManager:
    """Tracks application access sessions and security context layers safely."""

    def __init__(self) -> None:
        self._storage = FileStoreManager(USER_FILE)
        self._active_operator: Optional[OperatorUser] = None
        self._prime_default_admin()

    @property
    def current_operator(self) -> Optional[OperatorUser]:
        """Exposes context references for standard authentication verifications."""
        return self._active_operator

    def _hash_payload(self, raw_input: str) -> str:
        """Processes plain-text passwords into standard cryptographic strings."""
        return hashlib.sha256(raw_input.encode("utf-8")).hexdigest()

    def _prime_default_admin(self) -> None:
        """Primes systemic administrative user assets into target storage units if clean."""
        records = self._storage.read_records()
        if not any(item["email"] == "admin@library.com" for item in records):
            admin_payload = {
                "uid": "OP-001",
                "name": "System Administrator",
                "email": "admin@library.com",
                "secret_hash": self._hash_payload("admin123")
            }
            records.append(admin_payload)
            self._storage.write_records(records)

    @log_execution
    def register_operator(self, uid: str, name: str, email: str, standard_secret: str) -> None:
        """Registers a new administrative operator in the system records."""
        records = self._storage.read_records()
        if any(item["uid"] == uid or item["email"] == email for item in records):
            raise DuplicateRecordError("Operator structural indices match existing data rows inside identity indexes.")

        new_operator = {
            "uid": uid,
            "name": name,
            "email": email,
            "secret_hash": self._hash_payload(standard_secret)
        }
        records.append(new_operator)
        self._storage.write_records(records)

    @log_execution
    def authenticate(self, email: str, raw_secret: str) -> bool:
        """Validates incoming client credentials against standard encrypted entries."""
        records = self._storage.read_records()
        target_hash = self._hash_payload(raw_secret)
        for data in records:
            if data["email"] == email and data["secret_hash"] == target_hash:
                self._active_operator = OperatorUser(data["uid"], data["name"], data["email"], data["secret_hash"])
                return True
        return False

    def close_session(self) -> None:
        """Clears working identity tracking contexts entirely."""
        self._active_operator = None

    @log_execution
    def update_secret(self, current_raw: str, newly_created_raw: str) -> bool:
        """Updates internal authentication tracking elements for an operator."""
        if not self._active_operator:
            return False

        if self._active_operator.secret_hash != self._hash_payload(current_raw):
            return False

        records = self._storage.read_records()
        new_hash = self._hash_payload(newly_created_raw)

        for data in records:
            if data["uid"] == self._active_operator.identity_id:
                data["secret_hash"] = new_hash
                break

        self._storage.write_records(records)
        self._active_operator.secret_hash = new_hash
        return True