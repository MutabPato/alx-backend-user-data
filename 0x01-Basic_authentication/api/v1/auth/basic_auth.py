#!/usr/bin/env python3
""" Basic auth """

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar, Optional
from models.user import User

# Define a type variable with User as its bound
UserType = TypeVar('UserType', bound='User')


class BasicAuth(Auth):
    """ inherits from Auth """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Returns:
            Base64 part of the Authorization header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        # Extract Base64 part
        base64_part = authorization_header[6:]

        if not base64_part:
            return None

        return base64_part

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Returns:
            the decoded value of a Base64 string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded_authorization_header = base64.b64decode(
                    base64_authorization_header)
            authorization_header = encoded_authorization_header.decode('utf-8')
            return authorization_header

        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns:
            user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if decoded_base64_authorization_header.find(':') == -1:
            return (None, None)
        else:
            return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns:
            the User instance based on his email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users or not isinstance(users, list) or len(users) == 0:
            return None

        # Assume we take the first user in list
        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        header = self.authorization_header(request)
        extracted_header = self.extract_base64_authorization_header(header)
        decoded_header = self.decode_base64_authorization_header(
                extracted_header)
        extracted_credentials = self.extract_user_credentials(decoded_header)
        user_email, user_pwd = extracted_credentials
        user_credentials = self.user_object_from_credentials(
                user_email, user_pwd)

        return user_credentials
