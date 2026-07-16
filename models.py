"""
Domain entities mapping application domain structures.
Implements hierarchies, data models, constructors, and decorators.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any
from system_config import DATE_FORMAT

class Deserializable(ABC):
    """Enforces dynamic instantiations from standard mapped structural JSON entries."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Deserializable":
        """Reconstructs live concrete entity context records out of plain dictionary buffers."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Flattens runtime target objects down to structural dictionary payloads."""
        pass


class PrintableMixin:
    """Injects high-fidelity logging configurations across tracking entity elements dynamically."""

    def get_summary_string(self) -> str:
        """Standardized string processing vector utilizing metadata reflections."""
        attributes = ", ".join(f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_"))
        return f"[{self.__class__.__name__}({attributes})]"


class Identity(ABC):
    """Abstract core establishing fundamental structural identities for elements inside storage maps."""

    def __init__(self, identity_id: str) -> None:
        self._identity_id = identity_id

    @property
    def identity_id(self) -> str:
        """Exposes the raw foundational key string safely via standard encapsulation properties."""
        return self._identity_id

    @identity_id.setter
    def identity_id(self, val: str) -> None:
        self._identity_id = val

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Identity):
            return False
        return self._identity_id == other._identity_id

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} Bound Key Identification: {self._identity_id}>"


class AbstractBook(Identity, Deserializable, PrintableMixin, ABC):
    """Abstract structural base mapping cross-functional catalog core items."""

    def __init__(self, isbn: str, title: str, author: str, category: str, available_count: int) -> None:
        super().__init__(isbn)
        self.title = title
        self.author = author
        self.category = category
        self.available_count = available_count

    @abstractmethod
    def compute_risk_profile(self) -> str:
        """Determines tracking profiles based on material scarcity classifications."""
        pass


class Book(AbstractBook):
    """Standard inventory book component holding properties and dynamic values."""

    def __init__(self, isbn: str, title: str, author: str, category: str, available_count: int,
                 total_copies: int) -> None:
        super().__init__(isbn, title, author, category, available_count)
        self.total_copies = total_copies

    def compute_risk_profile(self) -> str:
        return "STANDARD_CIRCULATION" if self.total_copies > 2 else "HIGH_SCARCITY_TRACKED"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "isbn": self.identity_id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "available_count": self.available_count,
            "total_copies": self.total_copies
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Book":
        return cls(
            isbn=data["isbn"],
            title=data["title"],
            author=data["author"],
            category=data["category"],
            available_count=data["available_count"],
            total_copies=data["total_copies"]
        )

    def __str__(self) -> str:
        return f"'{self.title}' by {self.author} [ISBN: {self.identity_id}] (Avail: {self.available_count}/{self.total_copies})"

    def __len__(self) -> int:
        return self.available_count


class Profile(Identity, ABC):
    """System profile base establishing identity layers across users and personnel frameworks."""

    def __init__(self, uid: str, name: str, email: str) -> None:
        super().__init__(uid)
        self.name = name
        self.email = email


class Student(Profile, Deserializable, PrintableMixin):
    """Student profile tracking identification context and contact profiles."""

    def __init__(self, student_id: str, name: str, email: str, phone: str) -> None:
        super().__init__(student_id, name, email)
        self.phone = phone

    def to_dict(self) -> Dict[str, Any]:
        return {
            "student_id": self.identity_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"]
        )

    def __str__(self) -> str:
        return f"Student: {self.name} (ID: {self.identity_id}, Email: {self.email})"


class IssueTransaction(Identity, Deserializable):
    """Tracks state parameters across real-time historical book circulations."""

    def __init__(self, transaction_id: str, student_id: str, isbn: str, issue_date: datetime, due_date: datetime,
                 return_date: datetime | None = None) -> None:
        super().__init__(transaction_id)
        self.student_id = student_id
        self.isbn = isbn
        self.issue_date = issue_date
        self.due_date = due_date
        self.return_date = return_date

    @property
    def is_overdue(self) -> bool:
        """Evaluates live time metrics against constraints to isolate overdue state variables."""
        if self.return_date:
            return False
        return datetime.now() > self.due_date

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transaction_id": self.identity_id,
            "student_id": self.student_id,
            "isbn": self.isbn,
            "issue_date": self.issue_date.strftime(DATE_FORMAT),
            "due_date": self.due_date.strftime(DATE_FORMAT),
            "return_date": self.return_date.strftime(DATE_FORMAT) if self.return_date else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IssueTransaction":
        return cls(
            transaction_id=data["transaction_id"],
            student_id=data["student_id"],
            isbn=data["isbn"],
            issue_date=datetime.strptime(data["issue_date"], DATE_FORMAT),
            due_date=datetime.strptime(data["due_date"], DATE_FORMAT),
            return_date=datetime.strptime(data["return_date"], DATE_FORMAT) if data.get("return_date") else None
        )

    def __str__(self) -> str:
        status = f"Returned on {self.return_date}" if self.return_date else f"Due date: {self.due_date.strftime(DATE_FORMAT)}"
        return f"Tx: {self.identity_id} -> Student: {self.student_id}, Book ISBN: {self.isbn} ({status})"