import json
import os


class Student:
    def __init__(self, name, surname, age):
        self.name = name
        self.surname = surname
        self.age = age

    def __str__(self):
        return f"{self.name} | {self.surname} | {self.age}"


def create_database_file(filename):
    if os.path.exists(filename) is False:
        with open(filename, "w+") as file:
            data = {"students": []}
            json.dump(data, file)


class Database:
    def __init__(self, filename):
        self.filename = filename
        create_database_file(filename)

    def create(self, *args):
        try:
            student = Student(*args)
            with open(self.filename, "r+") as file:
                # Zalaczamy dane z pliku do zmiennej students
                data = json.load(file)
                data["students"].append(student.__dict__)
                file.seek(0)
                file.write(json.dumps(data))
                file.truncate()
        except Exception as e:
            print(e)

    # Wyszukujemy wszystkich uczniow
    def find_all(self, where=None):
        try:
            # Otwieramy baze
            with open(self.filename) as file:
                # Zalaczamy dane z pliku do zmiennej students
                data = json.load(file)
                return data["students"]
        except Exception as e:
            print(e)

    def find(self, where):
        try:
            with open(self.filename) as file:
                data = json.load(file)
                for student in data["students"]:
                    if student["name"] == where["name"] and student["surname"] == where["surname"]:
                        return Student(**student)
                return None
        except Exception as e:
            print(e)

    def delete(self, name, surname):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)

            with open(self.filename, "w") as file:
                for index, student in enumerate(data["students"]):
                    if student["name"] == name and student["surname"] == surname:
                        data["students"].pop(index)
                file.seek(0)
                file.write(json.dumps(data))
                file.truncate()

        except Exception as e:
            print(e)

    def update(self, name):
        pass
