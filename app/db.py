import json
import os


class User:
    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age

    def __str__(self):
        return f"{self.username} | {self.email} | {self.age}"


def handle_error(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(e)

    return wrapper


class Database:
    def __init__(self, filename):
        self.__filename = filename
        self.__create_database_file(filename)

    @staticmethod
    # Tworzomy nowy plik z danychmi jezeli nie istnieje
    def __create_database_file(filename):
        if os.path.exists(filename) is False:
            with open(filename, "w+") as file:
                data = {"users": []}
                json.dump(data, file)

    # Otwieramy plik i zwracamy jego dane
    def __load_data(self):
        with open(self.__filename, "r") as file:
            data = json.load(file)
            return data

    # Tworzomy uzytkownika
    @handle_error
    def create(self, *args):
        user = User(*args)
        with open(self.__filename, "r+") as file:
            # Zalaczamy dane z pliku do zmiennej students
            data = json.load(file)
            data["users"].append(user.__dict__)
            file.seek(0)
            file.write(json.dumps(data))
            file.truncate()
        return user

    @handle_error
    # Wyszukuemy uzytkownikow
    def find_all(self):
        data = self.__load_data()
        return data["users"]

    @handle_error
    # Wyszukumemy pojedynczego uzytytkownika
    def find(self, where):

        data = self.__load_data()
        username = where.get("username", None)
        email = where.get("email", None)
        user = None
        if username:
            user = [user for user in data["users"] if user["username"] == where["username"]]
        elif email:
            user = [user for user in data["users"] if user["email"] == email]
        return user[0] if len(user) else None

    @handle_error
    # Usuamy uzytkownika
    def delete(self, username):
        data = self.__load_data()
        with open(self.__filename, "w") as file:
            for index, user in enumerate(data["users"]):
                if user["username"] == username:
                    data["users"].pop(index)
            file.seek(0)
            file.write(json.dumps(data))
            file.truncate()

    @handle_error
    # Aktualizujemy uzytkownika
    def update(self, user, values):
        try:
            old_username = user.username
            user.username = values.get("username", user.username)
            user.email = values.get("email", user.email)
            user.age = values.get("age", user.age)

            self.delete(old_username)
            self.create(user.username, user.email, user.age)
        except Exception as e:
            print(e)


# Tworzomy nowa instacje bazy
db = Database("data.json")
