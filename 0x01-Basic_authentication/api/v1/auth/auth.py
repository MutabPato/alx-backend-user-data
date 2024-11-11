#!/usr/bin/env python3
"""Auth file
"""

from flask import request


class Auth:
    """Auth class
    """
    def __init__(self):
        """Initialize class
        """
        return

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Return:
        - False
        """
        Return False

    def authorization_header(self, request=None) -> str:
        """
        Return:
        - None
        """
        Return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
        - None
        """
        Return None
