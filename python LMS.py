import datetime

class LMS:
    """
    This class is used to keep a record of books in the library.
    It has modules: "Display Books", "Issue Books", "Return Books", "Add Books",
    "Add Member", "Member Information", "Delete Member", and "Transaction Tracking".
    """

    def __init__(self, list_of_books, library_name):
        self.list_of_books = list_of_books
        self.library_name = library_name
        self.books_dict = {}
        self.members_dict = {}
        self.transaction_history = []
        self.daily_late_fee = 50
        self.max_rent_fee = 500
        self.load_books()

    def load_books(self):
        """Load books from a text file."""
        try:
            with open(self.list_of_books, "r") as bk:
                content = bk.readlines()
                for idx, line in enumerate(content, start=101):
                    self.books_dict[str(idx)] = {
                        "books_title": line.strip(),
                        "lender_name": "",
                        "issue_date": "",
                        "status": "Available"
                    }
        except FileNotFoundError:
            print(f"Error: File '{self.list_of_books}' not found.")

    def display_books(self):
        """Display all books in the library."""
        print("------------------------- List of books ------------------------")
        print("Books ID", "\t", "Title")
        print("--------------------------------------------------------------")
        for key, value in self.books_dict.items():
            print(key, "\t\t", value["books_title"], "-[", value["status"], "]")

    def issue_books(self):
        """Issue a book to a member with a due date of 14 days from today."""
        books_id = input("Enter book ID: ")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if books_id in self.books_dict:
            if self.books_dict[books_id]['status'] != "Available":
                print(f"This book is already issued to {self.books_dict[books_id]['lender_name']} "
                      f"on {self.books_dict[books_id]['issue_date']}")
            else:
                your_name = input("Enter your name: ")
                self.books_dict[books_id].update({
                    "lender_name": your_name,
                    "issue_date": current_date,
                    "status": "Already Issued"
                })
                transaction = {
                    "transaction_type": "Issue",
                    "book_id": books_id,
                    "book_title": self.books_dict[books_id]['books_title'],
                    "member_name": your_name,
                    "issue_date": current_date,
                    "return_date": None,
                    "late_fee": 0
                }
                self.transaction_history.append(transaction)
                print("Book issued successfully!")
        else:
            print("Book ID not found.")
        
    
    def add_books(self):
        """Add a new book to the library."""
        new_books = input("Enter book title: ")
        if new_books == "":
            print("Book title cannot be empty. Try again.")
            return self.add_books()
        elif len(new_books) > 25:
            print("Book title length is too long! Title length should be 25 characters max.")
            return self.add_books()
        else:
            with open(self.list_of_books, "a") as bk:
                bk.write(f"{new_books}\n")
                new_id = str(int(max(self.books_dict.keys(), key=int)) + 1)
                self.books_dict[new_id] = {
                    "books_title": new_books,
                    "lender_name": "",
                    "issue_date": "",
                    "status": "Available"
                }
            print("Book added successfully!")


    def return_books(self):
        """Handle the return of books, calculate late fees if applicable."""
        book_id = input("Enter book ID: ")
        if book_id in self.books_dict:
            book = self.books_dict[book_id]
            if book["status"] == "Available":
                print("This book is already available in the library. Please check your book ID.")
            else:
                return_date = input("Enter return date (YYYY-MM-DD): ")
                try:
                    due_date = datetime.datetime.strptime(book["issue_date"], "%Y-%m-%d %H:%M:%S")
                    return_date = datetime.datetime.strptime(return_date, "%Y-%m-%d")
                    overdue_days = (return_date - due_date).days - 14
                    
                    fee = max(0, min(overdue_days * self.daily_late_fee, self.max_rent_fee)) if overdue_days > 0 else 0
                    if fee > 0:
                        print(f"Book '{book['books_title']}' is {overdue_days} days overdue.")
                        print(f"Late fee: ${fee}")
                    else:
                        print(f"Book '{book['books_title']}' returned on time. No late fee.")

                    self.books_dict[book_id].update({
                        "lender_name": "",
                        "issue_date": "",
                        "status": "Available"
                    })
                    transaction = {
                        "transaction_type": "Return",
                        "book_id": book_id,
                        "book_title": book['books_title'],
                        "member_name": book['lender_name'],
                        "issue_date": book["issue_date"],
                        "return_date": return_date.strftime("%Y-%m-%d"),
                        "late_fee": fee
                    }
                    self.transaction_history.append(transaction)
                    print("Successfully updated!")
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
        else:
            print("Book ID not found.")

    # Add similar corrections for other methods like `add_books`, `add_member`, etc.


try:
    myLMS = LMS("C:\\frape\\frappe_docker\\List_of_books.txt", "Python's Library")
    press_key_list = {
        "D": "Display Books", "I": "Issue Books", "A": "Add Books",
        "R": "Return Books", "Q": "Quit"
    }

    key_press = ""
    while key_press.lower() != "q":
        print(f"\n------------------- Welcome to {myLMS.library_name} Library management system --------- \n")
        for key, value in press_key_list.items():
            print(f"Press {key} To {value}")
        key_press = input("Press key: ").upper()

        if key_press == "I":
            print("\nCurrent Selection: Issue Books\n")
            myLMS.issue_books()
        elif key_press == "A":
            print("\nCurrent Selection: Add Book\n")
            myLMS.add_books()
        elif key_press == "D":
            print("\nCurrent Selection: Display Books\n")
            myLMS.display_books()
        elif key_press == "R":
            print("\nCurrent Selection: Return Books\n")
            myLMS.return_books()
        elif key_press == "Q":
            print("Exiting the system. Goodbye!")
        else:
            print("Invalid option, please try again.")

except Exception as e:
    print(f"Something went wrong: {e}")
