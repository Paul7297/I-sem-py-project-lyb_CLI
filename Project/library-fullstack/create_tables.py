# create_tables.py
from db_config import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            publication_year INT,
            book_type ENUM('Fiction', 'Non-Fiction', 'Reference'),
            is_available BOOLEAN DEFAULT TRUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fiction_books (
            book_id INT,
            genre VARCHAR(100),
            FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS non_fiction_books (
            book_id INT,
            subject VARCHAR(100),
            FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reference_books (
            book_id INT,
            field VARCHAR(100),
            FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(255),
            password VARCHAR(255) NOT NULL
        )
    """)
        # 🆕 Borrowed books table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrowed_books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        book_id INT NOT NULL,
        borrow_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        return_date DATETIME NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
    );
    """)
        # 🧑‍💼 Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        is_admin BOOLEAN DEFAULT FALSE
    );
    """)




    conn.commit()
    conn.close()
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    create_tables()
