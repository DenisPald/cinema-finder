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


def get_movie_number_keyboard() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()

    for i in range(1, 6):
        markup.add(
            types.InlineKeyboardButton(str(i),
                                       callback_data=film_cd.new(
                                           id="-1", action=str(i))))
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
        types.InlineKeyboardButton("Звезды",
                                   callback_data=film_cd.new(
                                       id=film_id, action="get stars")))
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
            "Похожее",
            callback_data=film_cd.new(id=film_id,
                                      action="get similars")))

    markup.add(
        types.InlineKeyboardButton("Назад к списку",
                                   callback_data=film_cd.new(
                                       id="-1", action="back to search list")))
    markup.add(
        types.InlineKeyboardButton("<< Главная <<",
                                   callback_data=film_cd.new(
                                       id="-1", action="get main page")))

    return markup
