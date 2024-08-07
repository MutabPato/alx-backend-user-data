#!/usr/bin/env python3
""" Basic auth """

from api.v1.auth.auth import Auth


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
