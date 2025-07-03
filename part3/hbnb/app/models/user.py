from app.models.baseEntity import (BaseEntity, type_validation,
                                   strlen_validation)
from validate_email_address import validate_email
import re
from app import bcrypt, db
from sqlalchemy import Column, Integer, String, DateTime
from .baseEntity import BaseEntity
from sqlalchemy.ext.hybrid import hybrid_property
from app.persistence.repository import SQLAlchemyRepository
from datetime import datetime, timezone
import uuid
from flask_bcrypt import generate_password_hash, check_password_hash


class User(BaseEntity):
    __tablename__ = 'users'

    id = db.Column(db.String(50), default=lambda:str(uuid.uuid4()), primary_key=True, nullable=False, unique=True)
    created_at = db.Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(String(128), nullable=False)

    def __init__(self, first_name: str, last_name: str,
                 email: str, is_admin: bool = False,
                 password: str = None):
        super().__init__()
        self.first_name = self.name_validation(first_name, "first_name")
        self.last_name = self.name_validation(last_name, "last_name")
        self.email = self.email_validation(email)
        self.is_admin = is_admin
        self.password = self.hash_password(password)

    def name_validation(self, names: str, names_name: str):
        type_validation(names, names_name, str)
        names = names.strip()
        strlen_validation(names, names_name, 1, 50)
        names_list = names.split()
        for name in names_list:
            if not re.match(r"^[^\W\d_]+([.'-][^\W\d_]+)*[.]?$", name,
                            re.UNICODE):
                raise ValueError(f"Invalid {names_name}: {names_name} "
                                 "must contain only letters, "
                                 "apostrophes, dashes, or dots (no "
                                 "digits or other special characters)")
        return " ".join(names_list)

    def email_validation(self, email: str):
        type_validation(email, "email", str)
        if not validate_email(email):
            raise ValueError("Invalid email: email must have format"
                             " example@exam.ple")
        return email

    def hash_password(self, plain_password):
        """Hashes the password before storing it"""
        if not isinstance(plain_password, str):
            raise TypeError("Password must be a string")
        return bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def verify_password(self, plain_password):
        """ Verifies if the provided password matches the hashed password"""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, plain_password)
    
    # def update_first_name(self, new_first_name):
    #     self.first_name = self.name_validation(new_first_name, "first_name")
