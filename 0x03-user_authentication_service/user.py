#!/usr/bin/env python3
"""
Defines a SQLAlchemy model for the `users` table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model for the `users` table.

    Attributes:
        id (int): The primary key, auto-incremented.
        email (str): The user's email (non-nullable).
        hashed_password (str): The hashed password (non-nullable).
        session_id (str): The current session ID (nullable).
        reset_token (str): Token for password reset (nullable).
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
