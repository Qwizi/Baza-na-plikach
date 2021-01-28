from app.actions import (
    FindAllUserAction,
    AddUserAction,
    FindUserAction,
    DeleteUserAction,
    UpdateUserUsernameAction,
    UpdateUserEmailAction,
    UpdateUserAgeAction
)
from app.menus import Menu
from app.messages import main_menu_messages


def create_menu():
    main_menu = Menu(main_menu_messages["title"])
    main_menu.add_option(main_menu_messages["find_all_option"], FindAllUserAction())
    main_menu.add_option(main_menu_messages["find_option"], FindUserAction())
    main_menu.add_option(main_menu_messages["add_option"], AddUserAction())
    main_menu.add_option(main_menu_messages["delete_option"], DeleteUserAction())
    main_menu.add_option(main_menu_messages["update_username_option"], UpdateUserUsernameAction())
    main_menu.add_option(main_menu_messages["update_email_option"], UpdateUserEmailAction())
    main_menu.add_option(main_menu_messages["update_age_option"], UpdateUserAgeAction())
    main_menu.add_exit_option()
    return main_menu


def main():
    main_menu = create_menu()
    main_menu.select_option()
