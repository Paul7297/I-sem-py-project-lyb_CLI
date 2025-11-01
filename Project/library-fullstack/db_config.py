# db_config.py
import mysql.connector

def get_connection():
    """Create and return a MySQL database connection."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",            # 🔹 change to your MySQL username
        password="25MCD10038",  # 🔹 change to your MySQL password
        database="library_db"      # 🔹 must exist already (we'll create it next)
    )
    return connection

