from abc import ABC, abstractmethod
from db import db
from exceptions import NotValidStudent

class Action(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError("Nie zaimplementowano metody")


class AddStudentAction(Action):
    def execute(self):
        data = str(input("Podaj imie, nazwisko, wiek oddzielajac je spacja: "))
        exploded_data = data.split(" ")
        if len(exploded_data) != 3:
            raise NotValidStudent("Błedne dane. Podaj imie, nazwisko, wiek oddzielajac je spacja")
        name = exploded_data[0]
        surname = exploded_data[1]
        age = exploded_data[2]

        student = db.create(name, surname, age)
        print(student)
