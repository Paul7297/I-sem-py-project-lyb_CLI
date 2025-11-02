# I-sem-py-project-lyb_CLI
# 📚 Library Management System (Python + MySQL)

A Library Management System built using **Python** and **MySQL**.  
This project allows users to register, log in, borrow, and return books, and enables an admin to manage all library operations.

---

## 🏫 Project Information
- **Student Name:** Vivek Raj  
- **Student ID:** 25MCD10038  
- **Course:** MCA (Data Science)  
- **University:** Chandigarh University  
- **Project Type:** Mini Project  
- **Semester:** [1st SEM]  

---

## ⚙️ Features

### 👤 User Features
- Register and log in securely (email validation included)
- View available books
- Borrow and return books
- View personal borrowed book history

### 🔐 Admin Features
- Admin login with special privileges
- View all borrowed books with user details
- Add, search, and delete books
- Manage all user activities

---

## 🧩 Tech Stack
- **Programming Language:** Python  
- **Database:** MySQL  
- **Libraries Used:**
  - `mysql.connector`
  - `re` (for email validation)
  - `datetime`
  
---

## 🗂️ Project Structure



---

## 💾 Database Setup (MySQL)

1. Open **MySQL Workbench** or terminal.
2. Create a new database:
   ```sql
   CREATE DATABASE library_db;
   USE library_db;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    publication_year INT,
    book_type VARCHAR(50)
);

CREATE TABLE borrowed_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    book_id INT,
    borrow_date DATETIME DEFAULT NOW(),
    return_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);
Optionally, make a user admin:
UPDATE users SET is_admin = TRUE WHERE username = 'admin_username';

▶️ How to Run
Clone the repository:
git clone [https://github.com/<your-username>/library-management-system.git](https://github.com/Paul7297/I-sem-py-project-lyb_CLI)

Navigate into the project folder:
cd library-management-system

Install dependencies:
pip install mysql-connector-python

Run the application:
python main.py


**Sample Outputs**
📚 Welcome to the Library System

1. User Login
2. Admin Login
3. Register User
4. Exit
Enter choice (or press Ctrl+C to quit): 



**Library Menu (User):**
📚 Library Menu:
1. Add New Book
2. Search for Book
3. List Available Books
4. Borrow Book
5. Return Book
6. View Borrowed Books
7. View All Books
9. Exit
Enter your choice (1–7 or 'q' to quit):

**Admin Menu:**
🔐 ADMIN MENU
1. View all borrowed books
2. View all books
3. Delete a book
4. Back to main menu
Enter your choice (1–4):


**Learning Outcomes**

Understanding of Python–MySQL integration

Database CRUD operations

User authentication system

Admin-user role management

Exception handling and input validation in Python

👉 [Click here to download ZIP](https://github.com/Paul7297/I-sem-py-project-lyb_CLI/blob/main/Project.zip)






