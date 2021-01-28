import json
import os


class User:
    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age

    def __str__(self):
        return f"{self.username} | {self.email} | {self.age}"


def create_database_file(filename):
    if os.path.exists(filename) is False:
        with open(filename, "w+") as file:
            data = {"users": []}
            json.dump(data, file)


class Database:
    def __init__(self, filename):
        self.filename = filename
        create_database_file(filename)

    def __load_data(self):
        with open(self.filename, "r") as file:
            data = json.load(file)
            return data

    def create(self, *args):
        try:
            user = User(*args)
            with open(self.filename, "r+") as file:
                # Zalaczamy dane z pliku do zmiennej students
                data = json.load(file)
                data["users"].append(user.__dict__)
                file.seek(0)
                file.write(json.dumps(data))
                file.truncate()
            return user
        except Exception as e:
            print(e)

    # Wyszukujemy wszystkich uczniow
    def find_all(self, where=None):
        try:
            # Otwieramy baze
            with open(self.filename) as file:
                # Zalaczamy dane z pliku do zmiennej students
                data = json.load(file)
                return data["users"]
        except Exception as e:
            print(e)

    def find(self, where):
        try:
            data = self.__load_data()
            for user in data["users"]:
                if user["username"] == where["username"]:
                    return user
            return None
        except Exception as e:
            print(e)

    def delete(self, username):
        try:
            data = self.__load_data()

            with open(self.filename, "w") as file:
                for index, user in enumerate(data["users"]):
                    if user["username"] == username:
                        data["users"].pop(index)
                file.seek(0)
                file.write(json.dumps(data))
                file.truncate()

        except Exception as e:
            print(e)

    def update(self, user, values):
        try:
            user.username = values.get("username", user.username)
            user.email = values.get("email", user.email)
            user.age = values.get("age", user.age)

            self.delete(user.username)
            self.create(user.username, user.email, user.age)
        except Exception as e:
            print(e)


db = Database("data.json")
