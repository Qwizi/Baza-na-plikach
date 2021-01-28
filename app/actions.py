import sys
from abc import ABC, abstractmethod
from app.db import db, User
from app.exceptions import InvalidUser, NotFoundUser, UserExists
from app.messages import (
    NOT_IMPLEMENTED_ERROR,
    ACTION_USER_ADD_MESSAGE,
    NOT_VALID_USER,
    NOT_FOUND_USER,
    TYPE_USERNAME,
    USER_EXISTS,
    EMPTY_USERS,
    NOT_VALID_ARGUMENT,
    NOT_VALID_AGE
)


def get_arguments(data):
    return data.split(" ")


def find_user_by_username_or_404(username):
    user = db.find(where={"username": username})
    if user is None:
        raise NotFoundUser(NOT_FOUND_USER)
    return User(**user)


def edit_user_values(value, msg):
    username = str(input(TYPE_USERNAME))
    user = find_user_by_username_or_404(username)
    print(f"Edytujesz uzytkownika: {user}")
    new_value = str(input(msg))
    db.update(user, values={value: new_value})
    returned_where = {"username": new_value if value == "username" else user.username}
    updated_user = db.find(where=returned_where)
    print(User(**updated_user))


class Action(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR)


class ExitProgramAction(Action):
    def execute(self):
        sys.exit()


class FindAllUserAction(Action):
    def execute(self):
        users = db.find_all()
        if not len(users):
            print(EMPTY_USERS)
        for user in users:
            print(User(**user))


class FindUserAction(Action):
    def execute(self):
        username = str(input(TYPE_USERNAME))
        user = find_user_by_username_or_404(username)
        print(user)


class AddUserAction(Action):
    def execute(self):
        data = str(input(ACTION_USER_ADD_MESSAGE))
        exploded_data = get_arguments(data)
        if len(exploded_data) != 3:
            raise InvalidUser(NOT_VALID_USER)

        username = exploded_data[0]
        email = exploded_data[1]
        age = exploded_data[2]

        inputs_to_check = [username, email, age]

        if not age.isnumeric():
            raise Exception(NOT_VALID_AGE)

        for item in inputs_to_check:
            if item == "":
                raise Exception(NOT_VALID_ARGUMENT)

        if db.find(where={"username": username}):
            raise UserExists(USER_EXISTS)

        user = db.create(username, email, age)
        print(user)


class DeleteUserAction(Action):
    def execute(self):
        username = str(input(TYPE_USERNAME))
        user = find_user_by_username_or_404(username)
        db.delete(user.username)
        print(f"Usunieto uzytkownika {user}")


class UpdateUserUsernameAction(Action):
    def execute(self):
        edit_user_values("username", "Podaj nowa nazwe uzytkownika: ")


class UpdateUserEmailAction(Action):

    def execute(self):
        edit_user_values("email", "Podaj nowy adres emial: ")


class UpdateUserAgeAction(Action):

    def execute(self):
        edit_user_values("age", "Podaj nowy wiek uzytkownika: ")
