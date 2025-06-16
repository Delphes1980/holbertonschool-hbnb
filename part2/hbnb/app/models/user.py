from hbnb.app.models.baseEntity import BaseEntity
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
            raise ValueError("Invalid email: non-empty email is "
                             "required")
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def name_validation(self, name: str, name_name: str):
        if not isinstance(name, str):
            raise TypeError(f"{name_name} must be a str")
        elif len(name) > 50 and len(name) == 0:
            raise ValueError(f"{name_name} must be shorter than 50 "
                             "characters and include at least 1"
                             "non-space character")

    def email_validation(self, email: str):
        if not isinstance(email, str):
            raise TypeError("email must be a str")
        elif not validate_email(email):
            raise ValueError("Invalid email: email must have format"
                             " example@example_dom.ain")
        print("Warning: email has not been verified for uniqueness "
              " despite it being absolutely necessary")

    @property
    def first_name(self):
        return self.__first_name
    @first_name.setter
    def first_name(self, first_name: str):
        self.name_validation(first_name.strip(), "First name")
        self.__first_name = first_name.strip()
    
    @property
    def last_name(self):
        return self.__last_name
    @last_name.setter
    def last_name(self, last_name: str):
        self.name_validation(last_name.strip(), "Last name")
        self.__last_name = last_name.strip()

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
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be boolean")
        self.__is_admin = is_admin

if __name__ == "__main__":
    user = User("John", "Smith", "john@smith.com")
    print(user.__dict__)
    print("User was successfully created")
