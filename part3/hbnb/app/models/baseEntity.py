import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True
    id = Column(String(50), default=uuid.uuid4, primary_key=True, nullable=False, unique=True)
    created_at = Column(DateTime = any, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(Datetime = any, nullable=False, default=lambda: datetime.now(timezone.utc))

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

    # def to_dict(self):
    #     """Convert the object to a dictionary representation"""
    #     return {
    #         "id": self.id,
    #         "created_at": self.created_at.isoformat(),
    #         "updated_at": self.updated_at.isoformat(),
    #     }


def type_validation(arg, arg_name: str, *arg_type):
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
    if len(string) < min_len or len(string) > max_len:
        raise ValueError(f"Invalid {string_name}: {string_name} must "
                         f"be shorter than {max_len} characters and "
                         f"include at least {min_len} non-space "
                         "characters")
