#!/usr/bin/env python3
"""Auth file
"""

from flask import request
from typing import List, TypeVar
import fnmatch


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
        if excluded_paths is None or not excluded_paths:
            return True
        
        if not path.endswith("/"):
            path += "/"

        for exclude_path in excluded_paths:
            # Handle paths ending with * as wildcard for prefix matching
            if exclude_path.endswith("*"):
                if path.startswith(exclude_path[:-1]):
                    return False
            elif path == exclude_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Return:
            None
        """
        if request is None:
            return None
        if request.headers.get("Authorization") is None:
            return None
        else:
            return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            None
        """
        return None
