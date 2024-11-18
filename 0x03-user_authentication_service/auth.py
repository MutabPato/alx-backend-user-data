#!/usr/bin/env python3


import bcrypt


def _hash_password(password: str) -> bytes:
    """Hasshes a password
    """
    p_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_p = bcrypt.hashpw(p_bytes, salt)

    return hash_p
