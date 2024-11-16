#!/usr/bin/env python3
"""SessionExpAuth file
"""

from typing import List, TypeVar
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class
    """
    def __init__(self):
        """Initialize class"""
        try:
            session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """Create a session with expiration
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve a user ID
        """
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        user_id = session_data.get("user_id")
        created_at = session_data.get("created_at")

        if user_id is None or created_at is None:
            return None

        # Check if session is expired
        if self.session_duration <= 0:
            return user_id

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            # Session expired, remove it from storage
            del self.user_id_by_session_id[session_id]
            return None

        return user_id
