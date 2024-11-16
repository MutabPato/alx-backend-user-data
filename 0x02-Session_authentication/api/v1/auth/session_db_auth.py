#!/usr/bin/env python3
"""SessionDBAuth file
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Create and store new session in the database
    """
    def create_session(self, user_id=None):
        """Create a session with expiration
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve a user ID
        """
        if session_id is None:
            return None

        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return None

        if not sessions or len(sessions) == 0:
            return None

        session = sessions[0]
        if self.session_duration <= 0:
            return session.user_id

        created_at = session.created_at
        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            # Session expired, remove it from storage
            session.remove()
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """destroys the UserSession based on the Session ID
        from the request cookie"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return False

        if not sessions or len(sessions) == 0:
            return False

        # Remove session from the database
        session = sessions[0]
        session.remove()
        return True
