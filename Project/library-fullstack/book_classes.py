# book_classes.py

class Book:
    def __init__(self, title, author, publication_year, book_type, is_available=True):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.book_type = book_type
        self.is_available = is_available

    def display_info(self):
        print(f"{self.title} by {self.author} ({self.publication_year}) - {self.book_type}")


class FictionBook(Book):
    def __init__(self, title, author, publication_year, genre, is_available=True):
        super().__init__(title, author, publication_year, "Fiction", is_available)
        self.genre = genre

    def display_info(self):
        super().display_info()
        print(f"Genre: {self.genre}")


class NonFictionBook(Book):
    def __init__(self, title, author, publication_year, subject, is_available=True):
        super().__init__(title, author, publication_year, "Non-Fiction", is_available)
        self.subject = subject

    def display_info(self):
        super().display_info()
        print(f"Subject: {self.subject}")


class ReferenceBook(Book):
    def __init__(self, title, author, publication_year, field, is_available=True):
        super().__init__(title, author, publication_year, "Reference", is_available)
        self.field = field

    def display_info(self):
        super().display_info()
        print(f"Reference Field: {self.field}")
