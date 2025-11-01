# user_auth.py
import mysql.connector
from db_config import get_connection
import hashlib

class UserAuth:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def hash_password(self, password):
        """Encrypt password before storing."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, email, password):
        try:
            hashed_pw = self.hash_password(password)

            # Check if username or email already exists
            self.cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            if self.cursor.fetchone():
                print("⚠️ Username or Email already exists.")
                return

            self.cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_pw)
            )
            self.conn.commit()
            print("✅ Registration successful!")
        except Exception as e:
            print(f"❌ Error registering user: {e}")

    def login_user(self, username, password):
        try:
            hashed_pw = self.hash_password(password)
            self.cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, hashed_pw)
            )
            user = self.cursor.fetchone()

            if user:
                print("✅ Login successful!")
                # return user["id"]  # ✅ Return user_id here
                return {"id": user["id"], "username": user["username"], "is_admin": user["is_admin"]}
            else:
                print("❌ Invalid username or password.")
                return None
        except Exception as e:
            print(f"❌ Error during login: {e}")
            return None

    def close(self):
        self.conn.close()
