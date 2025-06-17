import uuid
from datetime import datetime, timezone


class BaseEntity:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now(timezone.utc)

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

def type_validation(arg, arg_name: str, *arg_type):
    types_to_check = arg_type[0] if isinstance(arg_type[0], tuple) else arg_type
    if not isinstance(arg, types_to_check):
        if isinstance(types_to_check, tuple):
            type_list = [t.__name__ for t in types_to_check]
            types_string = " or ".join(type_list)
        else:
            types_string = types_to_check.__name__
        raise TypeError(f"{arg_name} must be of type {types_string}")

def strlen_validation(string: str, string_name: str, min_len, max_len):
    if len(string) < min_len or len(string) > max_len:
        raise ValueError(f"{string_name} must be shorter than "
                         f"{max_len} characters and include at" f"least {min_len} non-space character")
