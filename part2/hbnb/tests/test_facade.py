from app.services.facade import HBnBFacade

facade = HBnBFacade()

user_data = {"first_name": "John", "last_name": "Smith",
             "email": "john@example.com"}
someUser = facade.create_user(user_data)

print(someUser.__dict__)

retrievedUser = facade.get_user(someUser.id)

print(retrievedUser.__dict__)

retrievedUser2 = facade.get_user_by_email(someUser.email)

print(retrievedUser2.__dict__)
