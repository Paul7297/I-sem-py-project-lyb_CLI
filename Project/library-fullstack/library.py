# # library.py
# from db_config import get_connection
# from book_classes import FictionBook, NonFictionBook, ReferenceBook, Book

# class Library:
#     def __init__(self):
#         self.conn = get_connection()
#         self.cursor = self.conn.cursor()

#     # 🟢 Add a new book
#     def add_book(self, book):
#         query = """
#         INSERT INTO books (title, author, publication_year, book_type, is_available)
#         VALUES (%s, %s, %s, %s, %s)
#         """
#         values = (book.title, book.author, book.publication_year, book.book_type, book.is_available)
#         self.cursor.execute(query, values)
#         book_id = self.cursor.lastrowid

#         # Insert into specific table
#         if isinstance(book, FictionBook):
#             self.cursor.execute("INSERT INTO fiction_books (book_id, genre) VALUES (%s, %s)", (book_id, book.genre))
#         elif isinstance(book, NonFictionBook):
#             self.cursor.execute("INSERT INTO non_fiction_books (book_id, subject) VALUES (%s, %s)", (book_id, book.subject))
#         elif isinstance(book, ReferenceBook):
#             self.cursor.execute("INSERT INTO reference_books (book_id, field) VALUES (%s, %s)", (book_id, book.field))

#         self.conn.commit()
#         print("✅ Book added successfully!")

#     # 🟡 Search for books by keyword (title or author)
#     def search_books(self, keyword):
#         query = """
#         SELECT * FROM books
#         WHERE title LIKE %s OR author LIKE %s
#         """
#         like_keyword = f"%{keyword}%"
#         self.cursor.execute(query, (like_keyword, like_keyword))
#         results = self.cursor.fetchall()

#         if not results:
#             print("No books found.")
#             return

#         for row in results:
#             print(f"ID: {row[0]} | {row[1]} by {row[2]} ({row[3]}) | Type: {row[4]} | {'Available' if row[5] else 'Borrowed'}")

#     # 🔵 List all available books
#     def list_available_books(self):
#         self.cursor.execute("SELECT * FROM books WHERE is_available = TRUE")
#         results = self.cursor.fetchall()

#         if not results:
#             print("No available books right now.")
#             return

#         for row in results:
#             print(f"{row[1]} by {row[2]} ({row[3]}) | {row[4]}")

#     # 🔴 Borrow a book
#     def borrow_book(self, title):
#         self.cursor.execute("SELECT id, is_available FROM books WHERE title = %s", (title,))
#         result = self.cursor.fetchone()

#         if not result:
#             print("Book not found.")
#             return
#         if not result[1]:
#             print("Book is already borrowed.")
#             return

#         self.cursor.execute("UPDATE books SET is_available = FALSE WHERE id = %s", (result[0],))
#         self.conn.commit()
#         print(f"📘 You have borrowed '{title}'.")

#     # 🟢 Return a book
#     def return_book(self, title):
#         self.cursor.execute("SELECT id, is_available FROM books WHERE title = %s", (title,))
#         result = self.cursor.fetchone()

#         if not result:
#             print("Book not found.")
#             return
#         if result[1]:
#             print("Book was not borrowed.")
#             return

#         self.cursor.execute("UPDATE books SET is_available = TRUE WHERE id = %s", (result[0],))
#         self.conn.commit()
#         print(f"📗 You have returned '{title}'.")

#     # ⚫ Close connection
#     def close(self):
#         self.conn.close()



# NEW VERSION
import mysql.connector
from db_config import get_connection

class Library:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def add_book(self, book):
        query = """
        INSERT INTO books (title, author, publication_year, is_available, type, extra_info)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        book_type = type(book).__name__
        extra_info = getattr(book, "genre", None) or getattr(book, "subject", None) or getattr(book, "field", None)
        self.cursor.execute(query, (book.title, book.author, book.publication_year, True, book_type, extra_info))
        self.conn.commit()
        print("✅ Book added successfully!")

    def search_books(self, keyword):
        query = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s"
        self.cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        results = self.cursor.fetchall()
        if results:
            for book in results:
                status = "Available" if book["is_available"] else "Borrowed"
                print(f"{book['title']} by {book['author']} ({book['publication_year']}) - {status}")
        else:
            print("❌ No books found.")

    def list_available_books(self):
        self.cursor.execute("SELECT * FROM books WHERE is_available = TRUE")
        books = self.cursor.fetchall()
        if not books:
            print("❌ No available books.")
            return
        for book in books:
            print(f"{book['title']} by {book['author']} ({book['publication_year']})")

    def borrow_book(self, title, user_id):
        # Check if available
        self.cursor.execute("SELECT * FROM books WHERE title = %s AND is_available = TRUE", (title,))
        book = self.cursor.fetchone()
        if not book:
            print("❌ Book not available for borrowing.")
            return

        # Mark unavailable + record in borrowed_books
        self.cursor.execute("UPDATE books SET is_available = FALSE WHERE id = %s", (book["id"],))
        self.cursor.execute(
            "INSERT INTO borrowed_books (user_id, book_id) VALUES (%s, %s)",
            (user_id, book["id"])
        )
        self.conn.commit()
        print(f"📚 You have borrowed '{book['title']}' successfully!")

    def return_book(self, title, user_id):
        # Check if user borrowed it
        self.cursor.execute("""
            SELECT bb.id, b.id AS book_id FROM borrowed_books bb
            JOIN books b ON bb.book_id = b.id
            WHERE b.title = %s AND bb.user_id = %s AND bb.return_date IS NULL
        """, (title, user_id))
        record = self.cursor.fetchone()

        if not record:
            print("❌ No active borrow record found for this book.")
            return

        # Mark as returned
        self.cursor.execute("UPDATE books SET is_available = TRUE WHERE id = %s", (record["book_id"],))
        self.cursor.execute("UPDATE borrowed_books SET return_date = NOW() WHERE id = %s", (record["id"],))
        self.conn.commit()
        print(f"✅ You have returned '{title}' successfully!")

    def view_borrowed_books(self):
        query = """
        SELECT u.username, b.title, bb.borrow_date, bb.return_date
        FROM borrowed_books bb
        JOIN users u ON bb.user_id = u.id
        JOIN books b ON bb.book_id = b.id
        ORDER BY bb.borrow_date DESC;
        """
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        if not records:
            print("📭 No borrowed books yet.")
        else:
            for rec in records:
                status = "Returned" if rec["return_date"] else "Borrowed"
                print(f"{rec['title']} — by {rec['username']} on {rec['borrow_date']} ({status})")
    
    def view_user_borrowed_books(self, user_id):
        """USER: Show books borrowed by the currently logged-in user"""
        try:
            self.cursor.execute("""
                SELECT b.title, b.author, b.publication_year, br.borrow_date
                FROM borrowed_books br
                JOIN books b ON br.book_id = b.id
                WHERE br.user_id = %s AND br.return_date IS NULL
            """, (user_id,))
            borrowed = self.cursor.fetchall()

            if borrowed:
                print("\n📘 Your Borrowed Books:")
                for book in borrowed:
                    print(f" - {book['title']} by {book['author']} ({book['publication_year']}) | Borrowed on: {book['borrow_date']}")
            else:
                print("\nℹ️ You have not borrowed any books yet.")
        except Exception as e:
            print(f"❌ Error fetching your borrowed books: {e}")


    def list_all_books(self):
        """Show all books, whether borrowed or not."""
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        if books:
            print("\n📚 All Books:")
            for book in books:
                status = "✅ Available" if book["is_available"] else "❌ Borrowed"
                print(f"📖 {book['title']} by {book['author']} ({book['publication_year']}) - {status}")
        else:
            print("No books found in the library.")

    def delete_book(self, title):
        """Admin can delete a book."""
        self.cursor.execute("DELETE FROM books WHERE title = %s", (title,))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            print(f"🗑️ '{title}' has been deleted successfully.")
        else:
            print("⚠️ Book not found.")


    def close(self):
        self.conn.close()
