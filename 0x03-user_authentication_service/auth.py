#!/usr/bin/env python3
"""Authentication module for user management and security."""


import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Hasshes a password bcrypt.

    Args:
        password (str): The plain-text password.

    Returns:
        bytes: The hashed password.
    """
    p_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_p = bcrypt.hashpw(p_bytes, salt)

    return hash_p


def _generate_uuid() -> str:
    """
    Generates a new UUID.

    Returns:
        str: A string representation of the UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    Provides methods for user registration, login validation,
    session management, and password reset.
    """

    def __init__(self) -> None:
        """
        Initializes the Auth class with a database connection.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user.
        Args:
            email (str): The user's email.
            password (str): The user's plain-text password.

        Returns:
            User: The registered user object.

        Raises:
            ValueError: If a user with the given email already exists.
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
        Validates credentials.

        Args:
            email (str): The user's email.
            password (str): The user's plain-text password.

        Returns:
            bool: True if credentials are valid, otherwise False.
        """
        try:
            user = self._db.find_user_by(email=email)
            bytes_p = password.encode('utf-8')
            return bcrypt.checkpw(bytes_p, user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        Creates a new session for the user.

        Args:
            email (str): The user's email.

        Returns:
            Union[str, None]: The session ID if successful, otherwise None.
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
        Retrieves a user by session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            Union[User, None]: The user object if found, otherwise None.
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
        Destroys a user's session by setting the session ID to None.

        Args:
            user_id (int): The user's ID.
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception as e:
            print(f"Error destroying session: {e}")

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for a user.

        Args:
            email (str): The user's email.

        Returns:
            str: The reset token.

        Raises:
            ValueError: If no user is found with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError(f"No user found with email: {email}")

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password using a reset token.

        Args:
            reset_token (str): The reset token.
            password (str): The new plain-text password.

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hash_p = _hash_password(password)
            self._db.update_user(
                    user.id, hashed_password=hash_p, reset_token=None
                    )
        except NoResultFound:
            raise ValueError("Invalid reset token")
