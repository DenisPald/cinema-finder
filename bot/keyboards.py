from aiogram import types
from aiogram.utils.callback_data import CallbackData

# Callback data формата
# film:<id>:<action>
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
                                       id="-1", action="get favorite list")))
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
    markup.insert(
        types.InlineKeyboardButton("Удалить из закладок",
                                   callback_data=film_cd.new(
                                       id=film_id, action="delete from favorite")))
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

    markup.insert(
        types.InlineKeyboardButton("Русское описание",
                                   callback_data=film_cd.new(
                                       id=film_id, action="get local plot")))

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
        types.InlineKeyboardButton("Похожее",
                                   callback_data=film_cd.new(
                                       id=film_id, action="get similars")))

    markup.add(
        types.InlineKeyboardButton("<< Главная <<",
                                   callback_data=film_cd.new(
                                       id="-1", action="get main page")))

    return markup


def movies_list_keyboard(movies: list) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()

    for i in range(len(movies)):
        # Костыль из-за путаницы в названиях
        if "imdb_id" in movies[i]:
            id = movies[i]['imdb_id']
        else:
            id = movies[i]['id']

        markup.add(
            types.InlineKeyboardButton(movies[i]['title'],
                                       callback_data=film_cd.new(
                                           id=id, action="get movie by id")))

    markup.add(
        types.InlineKeyboardButton("<< Главная <<",
                                   callback_data=film_cd.new(
                                       id="-1", action="get main page")))
    return markup
