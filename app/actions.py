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
    TYPE_EMAIL,
    USER_EXISTS,
    EMPTY_USERS,
    NOT_VALID_ARGUMENT,
    NOT_VALID_AGE
)


def save_run_action(f):
    def wrapper(*args):
        try:
            f(*args)
            return setattr(args[0], "repeat_question", False)
        except Exception as e:
            print(e)
            setattr(args[0], "repeat_question", True)
    return wrapper


class Action(ABC):
    def __init__(self):
        self.repeat_question = False

    @abstractmethod
    def execute(self):
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR)

    def find_user_or_404(self):
        value = self.get_user_by_criterion()
        user = db.find(where={value["criterion"]: value["value"]})
        if user is None:
            raise NotFoundUser(NOT_FOUND_USER)

        return User(**user)

    def edit_user_values(self, value, msg):
        user = self.find_user_or_404()

        print(f"Edytujesz uzytkownika: {user}")

        new_value = str(input(msg))
        db.update(user, values={value: new_value})
        returned_where = {"username": new_value if value == "username" else user.username}
        updated_user = db.find(where=returned_where)
        print(User(**updated_user))

    @staticmethod
    def get_arguments(data):
        return data.split(" ")

    @staticmethod
    def get_user_by_criterion():
        username_criterion = "username"
        email_criterion = "email"
        criterion_list = [username_criterion, email_criterion]
        criterion_value = str(
            input(f"Podaj jakim kriterum chcesz wyszukac uzytkownika [{', '.join(criterion_list)}]: "))
        if criterion_value not in criterion_list:
            raise Exception("Takie kriterium nie istnieje")
        value = str(input(TYPE_USERNAME)) if criterion_value == username_criterion else str(input(TYPE_EMAIL))
        return {
            "value": value,
            "criterion": criterion_value
        }


class ExitProgramAction(Action):
    def execute(self):
        sys.exit()


class FindAllUserAction(Action):
    @save_run_action
    def execute(self):
        users = db.find_all()
        if not len(users):
            print(EMPTY_USERS)
        for user in users:
            print(User(**user))


class FindUserAction(Action):
    @save_run_action
    def execute(self):
        user = self.find_user_or_404()
        print(user)


class AddUserAction(Action):
    @save_run_action
    def execute(self):
        data = str(input(ACTION_USER_ADD_MESSAGE))
        exploded_data = self.get_arguments(data)
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
    @save_run_action
    def execute(self):
        user = self.find_user_or_404()
        db.delete(user.username)
        print(f"Usunieto uzytkownika {user}")


class UpdateUserUsernameAction(Action):
    @save_run_action
    def execute(self):
        self.edit_user_values("username", "Podaj nowa nazwe uzytkownika: ")


class UpdateUserEmailAction(Action):
    @save_run_action
    def execute(self):
        self.edit_user_values("email", "Podaj nowy adres emial: ")


class UpdateUserAgeAction(Action):
    @save_run_action
    def execute(self):
        self.edit_user_values("age", "Podaj nowy wiek uzytkownika: ")
