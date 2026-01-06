from app.user.services import UserServices
from app.onlineordering.services import MenuServices, OptionServices, OptionGroupServices, ItemServices


def get_user_service():
    return UserServices()


def get_option_service():
    return OptionServices()


def get_option_group_service():
    return OptionGroupServices()


def get_item_service():
    return ItemServices()


def get_menu_service():
    return MenuServices()
