"""
Data transformation module. Builds analytics matrices, historical tracking metrics,
and aggregates status parameters out of historical logs.
"""

from datetime import datetime
from typing import Dict, List, Any
from library import LibraryCoreEngine


class AnalyticsEngine:
    """Consolidates cross-sectional data logs into actionable analytics charts."""

    def __init__(self, engine: LibraryCoreEngine) -> None:
        self.engine = engine

    def get_issued_books_report(self) -> List[Dict[str, Any]]:
        """Processes active logs to build unified status matrices across outstanding files."""
        report = []
        for tx in self.engine.transactions.values():
            if tx.return_date is None:
                student = self.engine.students.get(tx.student_id)
                book = self.engine.books.get(tx.isbn)
                report.append({
                    "tx_id": tx.identity_id,
                    "student_name": student.name if student else "Unknown",
                    "book_title": book.title if book else "Unknown",
                    "due_date": tx.due_date
                })
        return report

    def get_overdue_books_report(self) -> List[Dict[str, Any]]:
        """Isolates active tracking entries that exceed operational calendar rules."""
        report = []
        now = datetime.now()
        for tx in self.engine.transactions.values():
            if tx.return_date is None and now > tx.due_date:
                student = self.engine.students.get(tx.student_id)
                book = self.engine.books.get(tx.isbn)
                days_late = (now - tx.due_date).days
                report.append({
                    "tx_id": tx.identity_id,
                    "student_name": student.name if student else "Unknown",
                    "book_title": book.title if book else "Unknown",
                    "days_late": days_late,
                    "accumulated_fine": days_late * 2.0
                })
        return report

    def generate_student_history(self, student_id: str) -> List[Dict[str, Any]]:
        """Filters transactional history logs to isolate a single tracking identity context."""
        history = []
        for tx in self.engine.transactions.values():
            if tx.student_id == student_id:
                book = self.engine.books.get(tx.isbn)
                history.append({
                    "tx_id": tx.identity_id,
                    "book_title": book.title if book else "Unknown",
                    "issue_date": tx.issue_date,
                    "status": "Returned" if tx.return_date else "Outstanding"
                })
        return history

    def compile_library_statistics(self) -> Dict[str, Any]:
        """Runs aggregation functions across structural datasets to yield core state metrics."""
        total_books = sum(b.total_copies for b in self.engine.books.values())
        avail_books = sum(b.available_count for b in self.engine.books.values())
        checked_out = total_books - avail_books
        total_students = len(self.engine.students)

        return {
            "total_catalog_volumes": total_books,
            "available_physical_units": avail_books,
            "checked_out_units": checked_out,
            "registered_student_profiles": total_students,
            "total_historical_transactions": len(self.engine.transactions)
        }

    def get_most_borrowed_books(self) -> List[Dict[str, Any]]:
        """Computes structural borrowing frequencies to determine popular inventory items."""
        counter: Dict[str, int] = {}
        for tx in self.engine.transactions.values():
            counter[tx.isbn] = counter.get(tx.isbn, 0) + 1

        sorted_ranks = sorted(counter.items(), key=lambda node: node[1], reverse=True)[:5]

        ranking_list = []
        for isbn, volume in sorted_ranks:
            book = self.engine.books.get(isbn)
            ranking_list.append({
                "isbn": isbn,
                "title": book.title if book else "Removed Catalog Item",
                "checkout_velocity_count": volume
            })
        return ranking_list