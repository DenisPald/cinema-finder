from aiogram.dispatcher.filters.state import State, StatesGroup


class Dialogs():
    main_page = "Главная страница\nЗдравствуйте снова, {name}"
    enter_movie_name = "Введите название фильма для поиска"
    wait_loading = "Подождите, идет загрузка"

    get_movies_search_result = "Вот что удалось найти на IMDB:"
    get_movies_get_number = "Введите номер фильма"

    get_movie_get_number_error = "Введите число"


class States(StatesGroup):
    get_movies = State()
    get_movie = State()
