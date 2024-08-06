#!/usr/bin/env python3
"""API authentication."""

from flask import request
from typing import List, TypeVar


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
        """ To be implemented """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ To be implemented """
        return None
