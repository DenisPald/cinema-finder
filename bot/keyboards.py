from aiogram import types
from aiogram.utils.callback_data import CallbackData

film_cd = CallbackData("film", "id", "action")


def get_main_keyboard() -> types.InlineKeyboardMarkup:
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
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton("<< Главная <<",
                                   callback_data=film_cd.new(
                                       id="-1", action="get main page")))

    return markup


def get_movie_info_keyboard(film_id) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton("Добавить в закладки",
                                   callback_data=film_cd.new(
                                       id=film_id, action="add to favorite")))
    markup.add(
        types.InlineKeyboardButton("Посмотреть трейлер(IMDB)",
                                   callback_data=film_cd.new(
                                       id=film_id, action="get trailer")))
    markup.add(
        types.InlineKeyboardButton("Посмотреть постеры",
                                   callback_data=film_cd.new(
                                       id=film_id, action="get posters")))
    markup.add(
        types.InlineKeyboardButton(
            "Оригинальное описание",
            callback_data=film_cd.new(id=film_id, action="get original plot")))
    markup.add(
        types.InlineKeyboardButton("Отзывы",
                                   callback_data=film_cd.new(
                                       id=film_id, action="get reviews")))
    markup.insert(
        types.InlineKeyboardButton("Оценки",
                                   callback_data=film_cd.new(
                                       id=film_id, action="get ratings")))
    markup.insert(
        types.InlineKeyboardButton("Награды",
                                   callback_data=film_cd.new(
                                       id=film_id, action="get rewards")))
    markup.add(
        types.InlineKeyboardButton(
            "Посетить страницу фильма на других сайтах",
            callback_data=film_cd.new(id=film_id,
                                      action="get external sites")))

    markup.add(
        types.InlineKeyboardButton("<< Главная <<",
                                   callback_data=film_cd.new(
                                       id="-1", action="get main page")))

    return markup
