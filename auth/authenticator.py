from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
import jwt
import datetime
from database.db_manager import get_session
from database.models import User
from config import settings

class Authenticator:
    def __init__(self, secret: str):
        self.secret = secret

    def signup(self, name: str, email: str, password: str):
        name = (name or "").strip()
        email = (email or "").strip()
        if not name:
            return False, "Name is required"

        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            return False, str(e)

        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters"

        with get_session() as db:
            if db.query(User).filter(User.email == email).first():
                return False, "Email already registered"

            u = User(
                name=name,
                email=email,
                password_hash=password  # store as plain text
            )
            db.add(u)
            db.commit()
            return True, "User registered successfully"

    def login(self, email: str, password: str):
        email = (email or "").strip()
        if not email or not password:
            return False, None, None, "Email and password are required"

        with get_session() as db:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return False, None, None, "User not found"

            if user.password_hash != password:
                return False, None, None, "Incorrect password"

            payload = {
                "user_id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            token = jwt.encode(payload, self.secret, algorithm="HS256")

            # Return only primitive data
            return True, {"id": user.id, "name": user.name, "email": user.email}, token, "Login successful"
