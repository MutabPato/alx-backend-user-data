#!/usr/bin/env python3
"""API authentication."""

from flask import request
from typing import List, TypeVar
import os


class Auth():
    """A class to manage the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Define which routes don't need authentication

        Args:
            path: path to check
            excluded_paths: paths that do not need authentication

        Returns:
            True if path requires authentication, False otherwise
        """
        if path is None or excluded_paths is None:
            return True

        path = path.rstrip('/')
        excluded_paths = [p.rstrip('/') for p in excluded_paths]

        if path not in excluded_paths:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """
        Request validation

        Args:
            request: request to validate

        Returns:
            None if request is None or
            request doesn’t contain the header key Authorization
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ To be implemented """
        return None

    def session_cookie(self, request=None):
        """
        Returns:
            returns a cookie value from a request
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME', '_my_session_id')

        return request.cookies.get(session_name)
