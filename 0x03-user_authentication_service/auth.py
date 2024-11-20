#!/usr/bin/env python3


import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """Hasshes a password
    """
    p_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_p = bcrypt.hashpw(p_bytes, salt)

    return hash_p


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_p = _hash_password(password)
            user = self._db.add_user(email, hash_p)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            bytes_p = password.encode('utf-8')
            return bcrypt.checkpw(bytes_p, user.hashed_password)

        except Exception:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """returns user's session ID as a string
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Finds user by session ID
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a session
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception as e:
            print(f"Error destroying session: {e}")

    def get_reset_password_token(self, email: string) -> str:
        """
        Generates reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError(f"No user found with email: {email}")
