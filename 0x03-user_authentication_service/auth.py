#!/usr/bin/env python3


import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hasshes a password
    """
    p_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_p = bcrypt.hashpw(p_bytes, salt)

    return hash_p


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:

        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_p = _hash_password(password)
            user = self._db.add_user(email, hash_p)
            return user
