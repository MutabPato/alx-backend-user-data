#!/usr/bin/env python3
"""Defines a SQLAlchemy model for the `users` table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """SQLAlchemy model for the `users` table.

    Attributes:
        __tablename__ (str): Name of the table in the database.
        id (int): The primary key.
        email (str): The user's email (non-nullable).
        hashed_password (str): The hashed password (non-nullable).
        session_id (str): The current session ID (nullable).
        reset_token (str): Token for password reset (nullable).
    """
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250), nullable=True)
    reset_token: str = Column(String(250), nullable=True)
