import sys

from app.actions import Action, ExitProgramAction
from app.exceptions import InvalidOption
from app.messages import NOT_FOUND_OPTION, SELECT_OPTIONS, EXIT_PROGRAM


class Menu:

    def __init__(self, title: str):
        self.__title = title
        self.__options = []
        self.__repeat_select_option = True

    def add_option(self, title: str, action: Action):
        try:
            number = self.__options[-1]["number"] + 1
        except IndexError:
            number = 1
        self.__options.append({
            "number": number,
            "title": title,
            "action": action
        })

    def get_option(self, number: int):
        for option in self.__options:
            if option["number"] == number:
                return option
        return None

    def __select_option(self):
        try:
            while self.__repeat_select_option:
                option_number = int(input(SELECT_OPTIONS))
                option = self.get_option(option_number)
                if option is None:
                    raise InvalidOption(NOT_FOUND_OPTION)
                action = option["action"]
                action.execute()
                if action.repeat_question:
                    while action.repeat_question:
                        action.execute()

                if not action.repeat_question:
                    self.show()
        except Exception as e:
            print(e)
            self.show()
            self.__select_option()
        except KeyboardInterrupt:
            sys.exit()

    def select_option(self):
        try:
            self.show()
            self.__select_option()
        except InvalidOption as e:
            print(e)
            self.__select_option()

    def show(self):
        print(self.__title + ": ")
        for option in self.__options:
            print(f"{option['number']} - {option['title']}", end='\n')

    def add_exit_option(self):
        return self.add_option(EXIT_PROGRAM, ExitProgramAction())
