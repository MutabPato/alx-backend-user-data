#!/usr/bin/env python3
"""Personal data"""


import bcrypt


def hash_password(password: str) -> str:
    """Encrypting passwords
    """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd
