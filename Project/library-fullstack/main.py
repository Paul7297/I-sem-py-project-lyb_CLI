from book_classes import FictionBook, NonFictionBook, ReferenceBook
from library import Library
from user_auth import UserAuth
import re

def show_admin_menu(library):
    while True:
        print("\n🔐 ADMIN MENU")
        print("1. View all borrowed books")
        print("2. View all books")
        print("3. Delete a book")
        print("4. Back to main menu")

        choice = input("Enter your choice (1–4): ").strip()

        if choice == "1":
            library.view_borrowed_books()
        elif choice == "2":
            library.list_all_books()  # new helper to show all, even borrowed ones
        elif choice == "3":
            title = input("Enter book title to delete: ")
            library.delete_book(title)
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice, try again.")

def main():
    auth = UserAuth()
    library = Library()

    print("\n📚 Welcome to the Library System")
    current_user_id = None  # 🔹 track logged-in user
    current_user = None

    try:
        # 🔐 Login or Register
        while True:
            print("\n1. User Login")
            print("2. Admin Login")
            print("3. Register User")
            print("4. Exit")
            choice = input("Enter choice (or press Ctrl+C to quit): ")


            if choice == "1":
                username = input("Username: ")
                password = input("Password: ")
                # ✅ FIX: store user_id returned by login_user
                user_data = auth.login_user(username, password)
                if user_data:
                    current_user_id = user_data["id"]
                    current_user = user_data
                    break
                else:
                    print("❌ Login failed. Try again.")
            
            elif choice == "2":  # Admin Login
                username = input("Admin Username: ")
                password = input("Password: ")
                user_data = auth.login_user(username, password)
                if user_data and user_data["is_admin"]:
                    current_user_id = user_data["id"]
                    current_user = user_data
                    print("✅ Logged in as admin.")
                    show_admin_menu(library)
                    continue  # return to login screen after admin menu closes
                else:
                    print("🚫 Invalid admin credentials.")
            elif choice == "3":
                username = input("Choose a username: ")

                # Validate email format
                while True:
                    email = input("Email: ")
                    # Simple email validation pattern
                    if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                        break
                    else:
                        print("❌ Invalid email format! Example: user@gmail.com")

                password = input("Choose a password: ")
                auth.register_user(username, email, password)

            elif choice == "4":
                print("👋 Goodbye!")
                auth.close()
                return
            else:
                print("❌ Invalid choice!")

        # 🧾 Main Library Menu (after login)
        while True:
            print("\n📚 Library Menu:")
            print("1. Add New Book")
            print("2. Search for Book")
            print("3. List Available Books")
            print("4. Borrow Book")
            print("5. Return Book")
            print("6. View Borrowed Books")
            print("7. View All Books")
            print("8. Admin Menu (Admins Only)")
            print("9. Exit")
            
            choice = input("Enter your choice (1–7 or 'q' to quit): ").strip().lower()

            if choice == "1":
                kind = input("Type (Fiction / Non-Fiction / Reference): ").strip().lower()
                title = input("Title: ")
                author = input("Author: ")
                year = int(input("Publication Year: "))

                if kind == "fiction":
                    genre = input("Genre: ")
                    book = FictionBook(title, author, year, genre)
                elif kind == "non-fiction":
                    subject = input("Subject: ")
                    book = NonFictionBook(title, author, year, subject)
                elif kind == "reference":
                    field = input("Reference Field: ")
                    book = ReferenceBook(title, author, year, field)
                else:
                    print("❌ Invalid type! Try again.")
                    continue

                library.add_book(book)

            elif choice == "2":
                keyword = input("Enter a keyword (title or author): ")
                library.search_books(keyword)

            elif choice == "3":
                library.list_available_books()

            elif choice == "4":
                title = input("Enter the title of the book to borrow: ")
                library.borrow_book(title, current_user_id)  # ✅ track who borrowed

            elif choice == "5":
                title = input("Enter the title of the book to return: ")
                library.return_book(title, current_user_id)  # ✅ track who returned
            
            elif choice == "6":
                # library.view_borrowed_books()  # ✅ All users can see borrowed list
                # ✅ Users see only their own borrowed books
                if current_user["is_admin"]:
                    library.view_borrowed_books()  # admin sees all
                else:
                    library.view_user_borrowed_books(current_user_id)  # user sees only their own

            elif choice == "7":
                library.list_all_books()  # ✅ All users can see all books


            elif choice == "8":
                # library.view_borrowed_books()  # ✅ UN COMMENT TO show all borrowed books with names BY ALL USER 
                if current_user["is_admin"]:
                    library.view_borrowed_books()
                    show_admin_menu(library)
                else:
                    print("🚫 Access denied! Only admin can view all borrowed books.")
            elif choice in ("9", "q"):
                library.close()
                auth.close()
                print("👋 Goodbye! Library closed.")
                break
            else:
                print("❌ Invalid choice! Please select between 1–7.")

    except KeyboardInterrupt:
        print("\n\n🛑 Program interrupted by user. Closing safely...")
        library.close()
        auth.close()

if __name__ == "__main__":
    main()
