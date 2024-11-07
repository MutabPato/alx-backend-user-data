#!/usr/bin/env python3
"""Personal data
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Encrypting passwords
    """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check valid password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
