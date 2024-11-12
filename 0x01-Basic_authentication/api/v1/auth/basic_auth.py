#!/usr/bin/env python3
"""BasicAuth file
"""

from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64


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
