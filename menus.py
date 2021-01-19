class Action:
    def execute(self):
        pass




class Menu:
    def __init__(self, title):
        self.title = title
        self.options = []

    def add_option(self, options):
        self.options.append({""})

    def show(self):
        print(f'/----{self.title}----\\')

        print(f'/--------------------\\')


main_menu = Menu("Menu glowne")
