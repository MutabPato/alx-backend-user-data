#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import Any


class DB:
    """DB class for managing user data in the database.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance and set up the SQLite database.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)  # Reset database
        Base.metadata.create_all(self._engine)  # Create all tables
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Returns a memoized session object for database operations.
        Creates a new session if one does not already exist.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.

        Raises:
            RuntimeError: If the user cannot be added due to a database error.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
            return new_user
        except Exception as e:
            self._session.rollback()  # Rollback in case of an error
            raise RuntimeError(f"Error adding user: {e}")

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary keyword arguments.

        Args:
            **kwargs: Column-value pairs to filter the User table.

        Returns:
            User: The first User object matching the filter criteria.

        Raises:
            InvalidRequestError: If no filter arguments are provided
            or the query fails.
            NoResultFound: If no user matches the provided criteria.
        """
        if not kwargs:
            raise InvalidRequestError("No filter arguments provided.")
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound(f"No user found with filter: {kwargs}")
        except Exception as e:
            raise InvalidRequestError(f"Invalid request: {e}")

    def update_user(self, user_id, **kwargs) -> None:
        """
        Updates a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Column-value pairs representing the attributes to update.

        Raises:
            ValueError: If an invalid attribute is provided.
            Exception: For other general errors during the update process.
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError(f"Invalid attribute: {key}")
                setattr(user, key, value)
            self._session.commit()

        except Exception as e:
            self._session.rollback()
            raise e
