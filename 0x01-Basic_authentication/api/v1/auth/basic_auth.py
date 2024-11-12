#!/usr/bin/env python3
"""BasicAuth file
"""

from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """Auth class
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Basic - Base64 part
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        else:
            return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Basic - Base64 decode
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64_authorization_header.encode("utf-8")
            string_bytes = base64.b64decode(base64_bytes)
            decoded_string = string_bytes.decode("utf-8")
            return decoded_string
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Basic - User credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if decoded_base64_authorization_header.find(":") == -1:
            return (None, None)
        else:
            credentials = decoded_base64_authorization_header.split(":")
            return (credentials[0], credentials[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Basic - User object
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        if not users:
            return None
        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request: str = None) -> TypeVar('User'):
        """ Basic - Overload current_user
        """
        auth_head = self.authorization_header(request)
        b64_auth_head = self.extract_base64_authorization_header(auth_head)
        decoded_b64_auth_head = self.decode_base64_authorization_header(
                b64_auth_head)
        email, password = self.extract_user_credentials(decoded_b64_auth_head)
        user_object = self.user_object_from_credentials(email, password)

        return user_object
