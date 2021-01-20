from actions import Action, AddStudentAction
from exceptions import NotValidStudent, OptionNotFound


class Menu:

    def __init__(self, title: str):
        self.title = title
        self.options = []

    def add_option(self, title: str, action: Action):
        try:
            number = self.options[-1]["number"] + 1
        except IndexError:
            number = 1
        self.options.append({
            "number": number,
            "title": title,
            "action": action
        })

    def get_option(self, number: int):
        for option in self.options:
            if option["number"] == number:
                return option
        return None

    def __select_option(self):
        try:
            while True:
                option_number = int(input("Wybierz opcje: "))
                option = self.get_option(option_number)
                if option is None:
                    raise OptionNotFound("Nie znaleziono takiej opcji")
                action = option["action"]
                action.execute()
                self.show()
        except NotValidStudent as e:
            print(e)
            self.__select_option()
        except ValueError as e:
            print(e)
            self.show()
            self.__select_option()

    def select_option(self):
        try:
            self.show()
            self.__select_option()
        except OptionNotFound as e:
            print(e)
            self.__select_option()

    def show(self):
        print(self.title + ": ")
        for option in self.options:
            print(f"{option['number']} - {option['title']}", end='\n')


main_menu = Menu("Menu glowne")
main_menu.add_option("Dodaj ucznia", AddStudentAction())
main_menu.add_option("Edytuj ucznia", AddStudentAction())
main_menu.add_option("Usun ucznia", AddStudentAction())
main_menu.add_option("Lista uczniów", AddStudentAction())
main_menu.add_option("Wybierz pojedynczego ucznia", AddStudentAction())
