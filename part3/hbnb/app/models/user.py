from app.models.baseEntity import (BaseEntity, type_validation,
                                   strlen_validation)
from validate_email_address import validate_email
import re
from app import bcrypt, db
from sqlalchemy import Column, Integer, String
from .baseEntity import BaseEntity


class User(BaseEntity):
    __tablename__ = 'users'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    hashed_password = db.Column(String(128), unique=True, nullable=False)

    def __init__(self, first_name: str, last_name: str,
                 email: str, is_admin: bool = False,
                 hashed_password: str = None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hashed_password = hashed_password

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

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        self.__first_name = self.name_validation(first_name,
                                                 "first_name")

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        self.__last_name = self.name_validation(last_name, "last_name")

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email: str):
        self.__email = self.email_validation(email)

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, is_admin: bool):
        type_validation(is_admin, "is_admin", bool)
        self.__is_admin = is_admin

    @property
    def hashed_password(self):
        return self.__hashed_password

    @hashed_password.setter
    def hash_password(self, password):
        """Hashes the password before storing it"""
        type_validation(password, "password", str)
        if not password:
            raise ValueError("Invalid Password")
        self.password = (
            bcrypt.generate_password_hash(password)
            .decode('utf-8')
        )

    def verify_password(self, password):
        """ Verifies if the provided password matches the hashed password"""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)
