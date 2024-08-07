#!/usr/bin/env python3
""" Basic auth """

from api.v1.auth.auth import Auth
import base64


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
