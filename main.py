"""
Main driver interface execution script.
Assembles menus, formats data matrices cleanly, and provides user interaction loops.
"""
import os
import sys

# Forces Python to look into your local directory first before checking Anaconda packages
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from datetime import datetime
from colorama import init, Fore, Style
from authentication import SessionManager
from library import LibraryCoreEngine
from reports import AnalyticsEngine
from utilities import ScreenContext, LibraryException

init(autoreset=True)


class ManagementConsoleApp:
    """Manages application rendering sequences, operational routing loops, and interactive views."""

    def __init__(self) -> None:
        self.session = SessionManager()
        self.engine = LibraryCoreEngine()
        self.analytics = AnalyticsEngine(self.engine)

    def print_banner(self, title: str) -> None:
        """Renders clear layout headers cleanly to track active operational zones."""
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{Fore.YELLOW}  {title.upper()}")
        print(f"{Fore.CYAN}{'=' * 60}\n")

    def read_input(self, prompt_str: str) -> str:
        """Pipes console parameters safely, filtering structural control errors."""
        try:
            val = input(f"{Fore.WHITE}{prompt_str}").strip()
            return val
        except (KeyboardInterrupt, EOFError):
            print(
                f"\n{Fore.RED}System terminal abort signal isolated. Exiting interface configuration parameters safely.")
            sys.exit(0)

    def run(self) -> None:
        """Main execution lifecycle routing loop."""
        while True:
            if not self.session.current_operator:
                self.render_authentication_menu()
            else:
                self.render_primary_dashboard()

    def render_authentication_menu(self) -> None:
        """Handles operator login authorization checkpoints."""
        ScreenContext.clear()
        self.print_banner("Library System Access Portal")
        print("1. Authenticate Operator Profile")
        print("2. Shutdown Console Layer")

        choice = self.read_input("Select Choice Entry Index: ")
        if choice == "1":
            email = self.read_input("Enter Email: ")
            secret = self.read_input("Enter Secret Token: ")
            if self.session.authenticate(email, secret):
                print(
                    f"\n{Fore.GREEN}Authentication confirmed. Welcoming Active Operator: {self.session.current_operator.name}")
                self.read_input("\nPress Enter to proceed into administrative layout configuration parameters...")
            else:
                print(f"\n{Fore.RED}Invalid security profile access tokens. Entry validation failed.")
                self.read_input("\nPress Enter to return...")
        elif choice == "2":
            print(f"\n{Fore.GREEN}Shutting down runtime loops cleanly. Goodbye.")
            sys.exit(0)

    def render_primary_dashboard(self) -> None:
        """Core routing dashboard layout matrix switcher."""
        ScreenContext.clear()
        operator = self.session.current_operator
        self.print_banner(f"Primary Control Desk - Operator: {operator.name if operator else 'Guest'}")

        print(f"{Fore.GREEN}Catalog Entities Handling:")
        print("  1. Append Book Record")
        print("  2. Edit Book Mapping Data")
        print("  3. Remove Book from Ledger")
        print("  4. View Catalog Records Table")

        print(f"\n{Fore.GREEN}Demographic Management Matrix:")
        print("  5. Register Student Profile")
        print("  6. Edit Student Attributes")
        print("  7. Remove Student Tracking Context")
        print("  8. View Student Demographics Roster")

        print(f"\n{Fore.GREEN}Circulation Systems Engine:")
        print("  9. Register New Media Issue Transaction")
        print(" 10. Process Returned Volumetric Units")
        print(" 11. Process Duration Term Extensions")

        print(f"\n{Fore.GREEN}Statistical Intelligence Units:")
        print(" 12. View Active Allocation Matrices")
        print(" 13. View Overdue Portfolio Lists")
        print(" 14. Query Single Student Transaction Logs")
        print(" 15. Compile Macro System Statistics")
        print(" 16. View Top High-Velocity Assets")

        print(f"\n{Fore.GREEN}Security Configurations Control:")
        print(" 17. Modify Active Access Secret Tokens")
        print(" 18. Destroy Session Context (Logout)")
        print(" 19. Close System Applications")

        choice = self.read_input("\nSelect Target Menu Sequence Directive [1-19]: ")
        self.execute_route(choice)

    def execute_route(self, choice: str) -> None:
        """Decoupled internal routing engine map."""
        try:
            method_name = f"_route_action_{choice}"
            handler = getattr(self, method_name, None)
            if handler:
                ScreenContext.clear()
                handler()
            else:
                print(f"\n{Fore.RED}Invalid programmatic routing token selected. Try again.")
        except LibraryException as system_error:
            print(f"\n{Fore.RED}Operational execution blocked: {system_error.message}")
        except Exception as unexpected_error:
            print(f"\n{Fore.RED}Fatal backend unmapped processing collision: {str(unexpected_error)}")
        self.read_input(f"\n{Fore.WHITE}Action completed. Press Enter to return to the operational center...")

    # --- ROUTING TARGET HANDLERS ---
    def _route_action_1(self) -> None:
        self.print_banner("Append Book Record")
        isbn = self.read_input("Enter Unique ISBN Key: ")
        title = self.read_input("Enter Title String: ")
        author = self.read_input("Enter Author Details: ")
        category = self.read_input("Enter Analytical Category: ")
        copies = int(self.read_input("Enter Target Volumetric Allocation Capacity: "))
        self.engine.append_book(isbn, title, author, category, copies)
        print(f"\n{Fore.GREEN}Item added to database storage maps successfully.")

    def _route_action_2(self) -> None:
        self.print_banner("Edit Book Mapping Data")
        isbn = self.read_input("Enter Target ISBN Reference Identifier: ")
        title = self.read_input("Enter Revised Title String: ")
        author = self.read_input("Enter Revised Author Details: ")
        category = self.read_input("Enter Revised Structural Category Tag: ")
        delta = int(self.read_input("Enter Allocation Matrix Adjustments (e.g., +2 or -1): "))
        self.engine.edit_book(isbn, title, author, category, delta)
        print(f"\n{Fore.GREEN}Book inventory data matrices successfully updated inside permanent records.")

    def _route_action_3(self) -> None:
        self.print_banner("Remove Book from Ledger")
        isbn = self.read_input("Enter Target Elimination Item ISBN Key: ")
        self.engine.remove_book(isbn)
        print(f"\n{Fore.GREEN}Item removed from inventory records successfully.")

    def _route_action_4(self) -> None:
        self.print_banner("Current Book Catalog Records View")
        print("Sorting Options: 1. Title Ascending | 2. Available Units Descending")
        sort_choice = self.read_input("Select Sorting Mode: ")

        books_list = list(self.engine.books.values())
        if sort_choice == "1":
            books_list.sort(key=lambda item: item.title.lower())
        elif sort_choice == "2":
            books_list.sort(key=lambda item: item.available_count, reverse=True)

        print(f"\n{'-' * 80}")
        print(f"{'ISBN Key':<15} | {'Title Data String':<30} | {'Author':<20} | {'Avail':<6}")
        print(f"{'-' * 80}")
        for book in books_list:
            print(
                f"{book.identity_id:<15} | {book.title[:28]:<30} | {book.author[:18]:<20} | {book.available_count:<6}")
        print(f"{'-' * 80}")

    def _route_action_5(self) -> None:
        self.print_banner("Register Student Profile")
        sid = self.read_input("Enter Student Unique Primary Code ID: ")
        name = self.read_input("Enter Complete Client Name Mapping String: ")
        email = self.read_input("Enter Digital Web Electronic Email Profile: ")
        phone = self.read_input("Enter Contact Communication Phone Line Vector: ")
        self.engine.append_student(sid, name, email, phone)
        print(f"\n{Fore.GREEN}Profile entry committed successfully.")

    def _route_action_6(self) -> None:
        self.print_banner("Edit Student Attributes")
        sid = self.read_input("Enter Target Identification Student Reference Key: ")
        name = self.read_input("Enter Revised Name: ")
        email = self.read_input("Enter Revised Email Address Vector: ")
        phone = self.read_input("Enter Revised Phone Target Matrix: ")
        self.engine.edit_student(sid, name, email, phone)
        print(f"\n{Fore.GREEN}Demographic record mutations applied to base configurations.")

    def _route_action_7(self) -> None:
        self.print_banner("Remove Student Tracking Context")
        sid = self.read_input("Enter Student Key Target to drop from database nodes: ")
        self.engine.remove_student(sid)
        print(f"\n{Fore.GREEN}Student account references pruned out of production data pools.")

    def _route_action_8(self) -> None:
        self.print_banner("Registered Student Demographics Roster")
        students = list(self.engine.students.values())
        print(f"{'-' * 80}")
        print(f"{'Profile Code':<15} | {'Full Operational Name':<25} | {'Electronic Email':<25}")
        print(f"{'-' * 80}")
        for s in students:
            print(f"{s.identity_id:<15} | {s.name[:23]:<25} | {s.email[:23]:<25}")
        print(f"{'-' * 80}")

    def _route_action_9(self) -> None:
        self.print_banner("Register New Media Issue Transaction")
        sid = self.read_input("Enter Recipient Student Primary Account ID: ")
        isbn = self.read_input("Enter Target Volume Identification ISBN: ")
        tx_id = self.engine.issue_book(sid, isbn)
        print(f"\n{Fore.GREEN}Transaction registered successfully. Tracking Token assigned: {tx_id}")

    def _route_action_10(self) -> None:
        self.print_banner("Process Returned Volumetric Units")
        tx_id = self.read_input("Enter Unique Transaction Reference Token: ")
        fines = self.engine.return_book(tx_id)
        if fines > 0:
            print(
                f"\n{Fore.RED}System identified transaction delay thresholds broken. Late Processing Penalty assessed: ${fines:.2f}")
        else:
            print(f"\n{Fore.GREEN}Item logged into processing centers cleanly. Zero balance penalties generated.")

    def _route_action_11(self) -> None:
        self.print_banner("Process Duration Term Extensions")
        tx_id = self.read_input("Enter Outstanding Active Transaction Key String: ")
        new_due = self.engine.renew_book(tx_id)
        print(
            f"\n{Fore.GREEN}Term extension processed smoothly. Revised deadline date configuration: {new_due.strftime('%Y-%m-%d')}")

    def _route_action_12(self) -> None:
        self.print_banner("Active Outstanding Material Allocations")
        records = self.analytics.get_issued_books_report()
        for item in records:
            print(
                f"Tx: {item['tx_id']} | Client: {item['student_name']} | Title: {item['book_title']} | Due: {item['due_date'].strftime('%Y-%m-%d')}")

    def _route_action_13(self) -> None:
        self.print_banner("Overdue Portfolio Delinquency Tracking")
        records = self.analytics.get_overdue_books_report()
        if not records:
            print(f"{Fore.GREEN}Zero exceptions detected across the active ledger portfolio mappings.")
            return
        for item in records:
            print(
                f"{Fore.RED}Tx Token: {item['tx_id']} | Client: {item['student_name']} | Title: {item['book_title']} | Overdue Days Count: {item['days_late']} | Fines: ${item['accumulated_fine']:.2f}")

    def _route_action_14(self) -> None:
        self.print_banner("Query Single Student Transaction Logs")
        sid = self.read_input("Enter Identification Student Code Parameter: ")
        records = self.analytics.generate_student_history(sid)
        print(f"\nHistorical interaction tracking ledger metrics mapped for student identity profile {sid}:")
        for log in records:
            print(
                f"  - [Token: {log['tx_id']}] Volume: {log['book_title']} | Timestamp: {log['issue_date'].strftime('%Y-%m-%d')} | Status Index: {log['status']}")

    def _route_action_15(self) -> None:
        self.print_banner("Macro System Statistics Summary Grid")
        stats = self.analytics.compile_library_statistics()
        for descriptor, calculation in stats.items():
            clean_lbl = descriptor.replace("_", " ").title()
            print(f"{clean_lbl:<40} : {calculation}")

    def _route_action_16(self) -> None:
        self.print_banner("Top High-Velocity Assets Ranking Matrix")
        ranks = self.analytics.get_most_borrowed_books()
        for idx, entry in enumerate(ranks, 1):
            print(
                f"Rank {idx}. [ISBN: {entry['isbn']}] '{entry['title']}' -> Cumulative Borrowing Cycles: {entry['checkout_velocity_count']}")

    def _route_action_17(self) -> None:
        self.print_banner("Modify Active Access Secret Tokens")
        old = self.read_input("Confirm Existing Authorization Code Phrase: ")
        new_secret = self.read_input("Type Proposed Secure Replacement Token Pass: ")
        if self.session.update_secret(old, new_secret):
            print(f"\n{Fore.GREEN}System security credentials updated successfully across local profiles.")
        else:
            print(f"\n{Fore.RED}Security token matching verification checks failed. Action aborted.")

    def _route_action_18(self) -> None:
        self.session.close_session()
        print(f"\n{Fore.GREEN}Session tracking contexts closed cleanly. Returning to primary gateway layer.")

    def _route_action_19(self) -> None:
        print(f"\n{Fore.GREEN}System applications shutting down cleanly. Terminal context released.")
        sys.exit(0)


if __name__ == "__main__":
    app = ManagementConsoleApp()
    app.run()