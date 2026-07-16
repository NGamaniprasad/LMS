"""
Core structural control subsystem.
Implements custom collection models and updates transaction processing pipelines.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Iterator, Any
from models import Book, Student, IssueTransaction
from file_handler import FileStoreManager
from system_config import BOOK_FILE, STUDENT_FILE, ISSUED_FILE, DEFAULT_RENEWAL_DAYS, MAX_BORROW_LIMIT, DAILY_FINE_RATE
from utilities import (
    log_execution, EntityNotFoundError, DuplicateRecordError,
    TransactionBlockedError, Validator
)


class CatalogIterator:
    """Custom iterator providing sequential access parsing routes down across memory nodes."""

    def __init__(self, items: List[Any]) -> None:
        self._items = items
        self._index = 0

    def __iter__(self) -> Iterator[Any]:
        return self

    def __next__(self) -> Any:
        if self._index < len(self._items):
            target = self._items[self._index]
            self._index += 1
            return target
        raise StopIteration


class LibraryCoreEngine:
    """Manages data structures, transaction state configurations, and updates inventory elements."""

    def __init__(self) -> None:
        self._book_handler = FileStoreManager(BOOK_FILE)
        self._student_handler = FileStoreManager(STUDENT_FILE)
        self._issue_handler = FileStoreManager(ISSUED_FILE)

        self.books: Dict[str, Book] = {}
        self.students: Dict[str, Student] = {}
        self.transactions: Dict[str, IssueTransaction] = {}

        self.synchronize_in_memory_state()

    def synchronize_in_memory_state(self) -> None:
        """Loads physical configurations out of storage layers into memory maps."""
        self.books = {d["isbn"]: Book.from_dict(d) for d in self._book_handler.read_records()}
        self.students = {d["student_id"]: Student.from_dict(d) for d in self._student_handler.read_records()}
        self.transactions = {d["transaction_id"]: IssueTransaction.from_dict(d) for d in
                             self._issue_handler.read_records()}

    def flush_books(self) -> None:
        """Pushes working data matrices back down out to configuration nodes."""
        self._book_handler.write_records([b.to_dict() for b in self.books.values()])

    def flush_students(self) -> None:
        """Pushes structural customer tracking definitions into persistent memory structures."""
        self._student_handler.write_records([s.to_dict() for s in self.students.values()])

    def flush_transactions(self) -> None:
        """Pushes transactional records safely out into target long-term data files."""
        self._issue_handler.write_records([t.to_dict() for t in self.transactions.values()])

    def get_books_iterator(self) -> CatalogIterator:
        """Creates custom processing pointers across internal structural elements safely."""
        return CatalogIterator(list(self.books.values()))

    # --- BOOK CRUD OPERATIONS ---
    @log_execution
    def append_book(self, isbn: str, title: str, author: str, category: str, total_copies: int) -> None:
        """Inserts a unique structural media unit safely into inventory systems."""
        if isbn in self.books:
            raise DuplicateRecordError(f"Target book matching key index record configuration '{isbn}' already tracked.")

        new_book = Book(isbn, title, author, category, total_copies, total_copies)
        self.books[isbn] = new_book
        self.flush_books()

    @log_execution
    def edit_book(self, isbn: str, title: str, author: str, category: str, extra_copies: int) -> None:
        """Modifies operational definitions for an existing inventory item."""
        if isbn not in self.books:
            raise EntityNotFoundError(f"Target book reference index record configuration '{isbn}' not mapped.")

        target = self.books[isbn]
        target.title = title
        target.author = author
        target.category = category

        if extra_copies != 0:
            if target.total_copies + extra_copies < (target.total_copies - target.available_count):
                raise TransactionBlockedError("Active checkouts exceed proposed structure adjustments.")
            target.total_copies += extra_copies
            target.available_count += extra_copies

        self.flush_books()

    @log_execution
    def remove_book(self, isbn: str) -> None:
        """Removes a targeted tracking entry cleanly if no pending transactions block the action."""
        if isbn not in self.books:
            raise EntityNotFoundError(f"Target book key string '{isbn}' not mapped inside system index caches.")
        if self.books[isbn].available_count != self.books[isbn].total_copies:
            raise TransactionBlockedError("Outstanding items checkouts blocks target deletion processing.")

        del self.books[isbn]
        self.flush_books()

    # --- STUDENT CRUD OPERATIONS ---
    @log_execution
    def append_student(self, student_id: str, name: str, email: str, phone: str) -> None:
        """Registers a unique system user, checking structural constraints before entry."""
        if student_id in self.students:
            raise DuplicateRecordError(f"Target student tracking reference code ID '{student_id}' matches mapped row.")

        Validator.validate_email(email)
        Validator.validate_phone(phone)

        new_student = Student(student_id, name, email, phone)
        self.students[student_id] = new_student
        self.flush_students()

    @log_execution
    def edit_student(self, student_id: str, name: str, email: str, phone: str) -> None:
        """Modifies customer registration information safely inside memory caches."""
        if student_id not in self.students:
            raise EntityNotFoundError(f"Student mapping data row linked with key identifier: '{student_id}' not found.")

        Validator.validate_email(email)
        Validator.validate_phone(phone)

        target = self.students[student_id]
        target.name = name
        target.email = email
        target.phone = phone
        self.flush_students()

    @log_execution
    def remove_student(self, student_id: str) -> None:
        """Removes a student mapping if there are no open transactions against their profile."""
        if student_id not in self.students:
            raise EntityNotFoundError(
                f"Student metadata row context linked with code identifier: '{student_id}' unmapped.")

        has_active = any(t.student_id == student_id and t.return_date is None for t in self.transactions.values())
        if has_active:
            raise TransactionBlockedError(
                "Outstanding borrowed elements exist under target student code structure index.")

        del self.students[student_id]
        self.flush_students()

    # --- TRANSACTION IMPLEMENTATIONS ---
    @log_execution
    def issue_book(self, student_id: str, isbn: str) -> str:
        """Processes dynamic checkout actions while maintaining real-time threshold metrics."""
        if student_id not in self.students:
            raise EntityNotFoundError("Target registration student validation tracking metadata record not mapped.")
        if isbn not in self.books:
            raise EntityNotFoundError(
                "Target core repository item catalog verification model matching key context unmapped.")

        book = self.books[isbn]
        if book.available_count <= 0:
            raise TransactionBlockedError(
                f"No active inventory units accessible for reservation matching index code: {isbn}")

        active_count = sum(
            1 for t in self.transactions.values() if t.student_id == student_id and t.return_date is None)
        if active_count >= MAX_BORROW_LIMIT:
            raise TransactionBlockedError(
                f"Client metrics hit structural parameters constraint caps: {MAX_BORROW_LIMIT} tracking allocations.")

        tx_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now()
        due = now + timedelta(days=DEFAULT_RENEWAL_DAYS)

        transaction = IssueTransaction(tx_id, student_id, isbn, now, due)
        self.transactions[tx_id] = transaction

        book.available_count -= 1

        self.flush_books()
        self.flush_transactions()
        return tx_id

    @log_execution
    def return_book(self, transaction_id: str) -> float:
        """Registers returns, recalculating inventory states and evaluating due-date penalty fees."""
        if transaction_id not in self.transactions:
            raise EntityNotFoundError(
                f"Transaction parameter key reference values: '{transaction_id}' unmapped inside journals.")

        tx = self.transactions[transaction_id]
        if tx.return_date is not None:
            raise TransactionBlockedError(
                "Transaction registry ledger indicates historical target entry already returned.")

        now = datetime.now()
        tx.return_date = now

        book = self.books[tx.isbn]
        book.available_count += 1

        fine = 0.0
        if now > tx.due_date:
            days_overdue = (now - tx.due_date).days
            fine = days_overdue * DAILY_FINE_RATE

        self.flush_books()
        self.flush_transactions()
        return fine

    @log_execution
    def renew_book(self, transaction_id: str) -> datetime:
        """Extends operational deadline configurations if items remain clean of profile holds."""
        if transaction_id not in self.transactions:
            raise EntityNotFoundError(f"Target action transaction trace indicator token '{transaction_id}' not found.")

        tx = self.transactions[transaction_id]
        if tx.return_date is not None:
            raise TransactionBlockedError("Cannot process duration extensions on finished transaction profiles.")

        if datetime.now() > tx.due_date:
            raise TransactionBlockedError("Overdue parameters detected; clear outstanding item fees before extension.")

        tx.due_date = tx.due_date + timedelta(days=DEFAULT_RENEWAL_DAYS)
        self.flush_transactions()
        return tx.due_date