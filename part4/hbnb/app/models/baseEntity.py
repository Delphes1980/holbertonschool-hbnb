import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
from app import db


class BaseEntity(db.Model):
    # This ensures SQLAlchemy does not create a table for BaseModel
    __abstract__ = True
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()),
                   primary_key=True, nullable=False, unique=True)
    created_at = db.Column(DateTime, nullable=False,
                           default=datetime.now(timezone.utc))
    updated_at = db.Column(DateTime, nullable=False,
                           default=datetime.now(timezone.utc),
                           onupdate=datetime.now(timezone.utc))

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now(timezone.utc)

    def update(self, data):
        """Update the attributes of the object based on the
        provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp


def type_validation(arg, arg_name: str, *arg_type):
    """ Validates if an argument is of the expected type
    Args:
        arg: the argument to validate
        arg_name (str): the name of the argument
        *arg_type: one or more expected types
    Raises:
        TypeError: If the argument's type doesn't match the expected type"""
    types_to_check = arg_type[0] if isinstance(arg_type[0],
                                               tuple) else arg_type
    if not isinstance(arg, types_to_check):
        if isinstance(types_to_check, tuple):
            type_list = [t.__name__ for t in types_to_check]
            types_string = " or ".join(type_list)
        else:
            types_string = types_to_check.__name__
        raise TypeError(f"Invalid {arg_name}: {arg_name} must be of "
                        f"type {types_string}")


def strlen_validation(string: str, string_name: str, min_len, max_len):
    """ Validates the length of a specific range
    Args:
        string (str): the string to validate
        string_name (str): the name of the string
        min_len (int): the minimum length allowed for the string
        max_len (int): the maximum length allowed for the string
    Raises:
    ValueError: If the string's length length is outside the specified min_len
    and max_len"""
    if len(string) < min_len or len(string) > max_len:
        raise ValueError(f"Invalid {string_name}: {string_name} must "
                         f"be shorter than {max_len} characters and "
                         f"include at least {min_len} non-space "
                         "characters")
