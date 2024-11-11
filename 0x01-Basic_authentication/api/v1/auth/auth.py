#!/usr/bin/env python3
"""Auth file
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns:
            False
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        path = path if path.endswith('/') else path + '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Return:
            None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            None
        """
        return None
