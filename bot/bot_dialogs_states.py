from aiogram.dispatcher.filters.state import State, StatesGroup


class Dialogs():
    main_page = "Главная страница\nЗдравствуйте снова, {name}"
    enter_movie_name = "Введите название фильма для поиска"
    wait_loading = "Подождите, идет загрузка"

    get_movies_search_result = "Вот что удалось найти на IMDB"
    get_movies_get_number = "Выберите фильм"

    get_posters_ok = "Постеры"

    get_movie_get_number_error = "Введите число"

    similars = "Похожее:"

    list_of_favorite = "Ваши закладки"
    empty_list_of_favorite = "У вас пока нет закладок"

    error_message = "Произошла ошибка"
    error_not_founded = "Ничего не найдено"
    error_picture_loading = "Ошибка при загрузке постеров"

    success_adding_movie = "Успешно добавлено в ваши закладки"
    success_deleting_movie= "Успешно удалено из ваших закладок"

class States(StatesGroup):
    get_movies = State()
    get_movie = State()
    get_movie_info = State()
    checking_movie = State()
