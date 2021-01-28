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
    EMPTY_USERS
)


def get_arguments(data):
    return data.split(" ")


def find_user_by_username_or_404(username):
    user = db.find(where={"username": username})
    if user is None:
        raise NotFoundUser(NOT_FOUND_USER)
    return user


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
        print(User(**user))


class AddUserAction(Action):
    def execute(self):
        data = str(input(ACTION_USER_ADD_MESSAGE))
        exploded_data = get_arguments(data)
        if len(exploded_data) != 3:
            raise InvalidUser(NOT_VALID_USER)

        username = exploded_data[0]
        email = exploded_data[1]
        age = exploded_data[2]

        if db.find(where={"username": username}):
            raise UserExists(USER_EXISTS)

        user = db.create(username, email, age)
        print(user)


class DeleteUserAction(Action):
    def execute(self):
        username = str(input(TYPE_USERNAME))
        user = find_user_by_username_or_404(username)
        user = User(**user)
        db.delete(username)
        print(f"Usunieto uzytkownika {user}")

