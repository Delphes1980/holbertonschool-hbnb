from hbnb.app.models.baseEntity import BaseEntity, type_validation
from validate_email_address import validate_email


class User(BaseEntity):
    """ Missing error handles:
            - special characters in names
    """
    def __init__(self, first_name: str, last_name: str,
                 email: str, is_admin: bool = False):
        if not first_name:
            raise ValueError("First name is required")
        if not last_name:
            raise ValueError("Last name is required")
        if not email:
            raise ValueError("Invalid email: email is required")
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def name_validation(self, name: str, name_name: str):
        type_validation(name, name_name, str)
        max_length = 20
        min_length = 1
        name = name.strip()
        if len(name) < min_length or len(name) > max_length:
            raise ValueError(f"{name_name} must be shorter than {max_length} "
                             "characters and include at least {min_length} "
                             "non-space character")
        return name

    def email_validation(self, email: str):
        type_validation(email, "email", str)
        if not validate_email(email):
            raise ValueError("Invalid email: email must have format"
                             " example@example_dom.ain")
        print("Warning: email has not been verified for uniqueness "
              " despite it being absolutely necessary")

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name: str):
        self.__first_name = self.name_validation(first_name, "First name")

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name: str):
        self.__last_name = self.name_validation(last_name, "Last name")

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email: str):
        self.email_validation(email)
        self.__email = email

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, is_admin: bool):
        type_validation(is_admin, "is_admin", bool)
        self.__is_admin = is_admin
