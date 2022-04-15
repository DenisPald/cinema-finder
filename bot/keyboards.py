from aiogram import types
from aiogram.utils.callback_data import CallbackData

film_cd = CallbackData("film", "id", "action")


def get_main_keyboard() -> types.InlineKeyboardMarkup:
    """get main page keyboard

    :rtype: types.InlineKeyboardMarkup
    """
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton("Поиск",
                                   callback_data=film_cd.new(
                                       id="-1", action="get search page")))

    markup.add(
        types.InlineKeyboardButton("Мои закладки",
                                   callback_data=film_cd.new(
                                       id="-1", action="get user movies")))
    return markup


def get_search_keyboard() -> types.InlineKeyboardMarkup:
    """get search page keyboard

    :rtype: types.InlineKeyboardMarkup
    """
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton("<< Главная <<",
                                   callback_data=film_cd.new(
                                       id="-1", action="get main page")))

    return markup
