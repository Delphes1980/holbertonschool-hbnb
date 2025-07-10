from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def get_user(self, user_id):
        return self.model.query(User).filter_by(user_id).first()

    def get_all_users(self):
        return self.model.query(User).all()

    def create_user(self, user_data):
        new_user = User(user_data)
        self.model.add(new_user)
        return new_user

    def update_user(self, user_id, user_data):
        user_update = self.model.query(User).filter_by(user_id).first()
        if user_update:
            self.model.update(user_update, user_data)
            return user_update
        return None

    def delete_user(self, user_id):
        user_to_delete = self.model.query(User).filter_by(user_id).first()
        if user_to_delete:
            self.model.delete(user_to_delete)
            return True
        return False
