from .baseEntity import (BaseEntity, type_validation,
                                   strlen_validation)
from validate_email_address import validate_email
from app import bcrypt
import re
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Boolean
from sqlalchemy.ext.hybrid import hybrid_property


class User(BaseEntity):
    __tablename__ = 'users'

    _first_name: Mapped[str] = mapped_column("first_name",
                                             String(50),
                                             nullable=False)
    _last_name: Mapped[str] = mapped_column("last_name",
                                            String(50), nullable=False)
    _email: Mapped[str] = mapped_column("email",
                                        String(120), 
                                        nullable=False, unique=True)
    _password: Mapped[str] = mapped_column("password",
                                           String(128), nullable=False)
    _is_admin: Mapped[bool] = mapped_column("is_admin",
                                            Boolean, default=False)

    def __init__(self, first_name: str, last_name: str,
                 email: str, password: str, is_admin: bool = False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = password

    @hybrid_property
    def password(self): # type: ignore
        return self._password
    
    @password.setter
    def password(self, value):
        if value is None:
            raise ValueError('Expected password but received None')
        type_validation(value, 'password', str)
        self._password = self.hash_password(value)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        if password is None:
            raise ValueError('Expected password but received None')
        return bcrypt.generate_password_hash(password).\
            decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided pw matches the hashed password."""
        if password is None:
            raise ValueError('Expected password but received None')
        return bcrypt.check_password_hash(self.password, password)

    def name_validation(self, names: str, names_name: str):
        if names is None:
            raise ValueError(f'Expected {names_name} but received None')
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
        if email is None:
            raise ValueError('Expected email but received None')
        type_validation(email, "email", str)
        if not validate_email(email):
            raise ValueError("Invalid email: email must have format"
                             " example@exam.ple")
        return email

    @hybrid_property
    def first_name(self): # type: ignore
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = self.name_validation(value,
                                                 "first_name")

    @hybrid_property
    def last_name(self): # type: ignore
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = self.name_validation(value, "last_name")

    @hybrid_property
    def email(self): # type: ignore
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = self.email_validation(value)

    @hybrid_property
    def is_admin(self): # type: ignore
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value: bool):
        if value is None:
            raise ValueError('Expected boolean but received None')
        type_validation(value, "is_admin", bool)
        self._is_admin = value
