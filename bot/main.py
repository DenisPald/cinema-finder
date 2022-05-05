import logging

import dotenv
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from bot_dialogs_states import Dialogs, States
from data import MovieInfo
from keyboards import (film_cd, get_main_keyboard, get_movie_info_keyboard,
                       get_movie_number_keyboard, get_search_keyboard,
                       movies_list_keyboard)
from urls import Urls

config = dotenv.dotenv_values('.env')
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = config['TELEGRAM_TOKEN']
IMDB_TOKEN = config['IMDB_TOKEN']
API_HOST = config['API_HOST']

storage = MemoryStorage()

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    try:
        requests.post(
            Urls.register.format(api_uri=API_HOST,
                                 telegram_id=message.from_user.id))
    except Exception as e:
        await message.answer(Dialogs.error_message)
        return

    await message.answer(
        Dialogs.main_page.format(name=message.from_user.full_name),
        reply_markup=get_main_keyboard())


@dp.callback_query_handler(film_cd.filter(action='get main page'), state="*")
async def query_main(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(
        Dialogs.main_page.format(name=query.from_user.full_name),
        reply_markup=get_main_keyboard())

    if state:
        await state.finish()


@dp.callback_query_handler(film_cd.filter(action='get favorite list'),
                           state="*")
async def query_favorite_list(query: types.CallbackQuery, state: FSMContext):

    await States.checking_movie.set()

    data = requests.get(
        Urls.get_user_info.format(api_uri=API_HOST,
                                  id=query.from_user.id)).json()

    if data["error"] == "":
        await query.message.edit_text(Dialogs.list_of_favorite,
                                      reply_markup=movies_list_keyboard(
                                          data['info']['watch_item']))
    else:
        await query.message.edit_text(Dialogs.empty_list_of_favorite,
                                      reply_markup=get_main_keyboard())


@dp.message_handler(commands=['exit'], state="*")
async def cmd_main(message: types.Message, state: FSMContext):
    await message.answer(
        Dialogs.main_page.format(name=message.from_user.full_name),
        reply_markup=get_main_keyboard())
    if state:
        await state.finish()


@dp.callback_query_handler(film_cd.filter(action='get search page'), state="*")
async def query_search_page(query: types.CallbackQuery):
    await query.message.edit_text(Dialogs.enter_movie_name,
                                  reply_markup=get_search_keyboard())

    await States.get_movies.set()


@dp.message_handler(state=States.get_movies)
async def state_get_movies(message: types.Message, state: FSMContext):

    wait_message = await message.answer(Dialogs.wait_loading)
    await types.ChatActions.upload_photo()

    title = message.text
    data = requests.get(
        Urls.search_by_title.format(title=title, imdb_token=IMDB_TOKEN))
    if not data.ok:
        return
    data = data.json()

    if data['errorMessage'] != "":
        await message.answer(Dialogs.error_message)
        return

    if len(data['results']) == 0:
        await message.answer(Dialogs.error_not_founded)
        return

    storage = await dp.storage.get_data(chat=message.from_user.id)

    try:
        media = types.MediaGroup()
        for i in data['results'][:5]:
            media.attach_photo(i['image'], i['title'] + i['description'])

        await message.answer_media_group(media)
    except Exception as e:
        await message.answer(Dialogs.error_picture_loading)

    text = Dialogs.get_movies_search_result + "\n" + Dialogs.get_movies_get_number

    await message.answer(text=text,
                         reply_markup=get_movie_number_keyboard(
                             data['results'][:5]))
    await wait_message.delete()

    storage['search_result'] = data['results'][:5]

    await dp.storage.update_data(chat=message.from_user.id, data=storage)

    await States.get_movie.set()


@dp.callback_query_handler(state=States.get_movie)
async def query_get_movie(query: types.CallbackQuery, state: FSMContext):
    storage = await dp.storage.get_data(chat=query.from_user.id)

    number = int(query.data.split(":")[2]) - 1
    id = storage['search_result'][number]['id']
    data = requests.get(Urls.get_full_data.format(
        id=id, imdb_token=IMDB_TOKEN)).json()

    if data['errorMessage']:
        await query.answer(Dialogs.error_message)
        return

    if data['plotLocal']:
        await query.message.edit_text(data['fullTitle'] + "\n" +
                                      data['plotLocal'])
    else:
        await query.message.edit_text(data['fullTitle'] + "\n" + data['plot'])

    await query.message.edit_reply_markup(get_movie_info_keyboard(id))

    storage['current_movie_data'] = MovieInfo(
        data['id'], data['fullTitle'], data['trailer']['linkEmbed'],
        data['posters']['posters'][:5], data['plot'], data['awards'],
        data['ratings'], data['stars'], data['similars'][:5],
        data['plotLocal'])

    await dp.storage.update_data(chat=query.from_user.id, data=storage)

    await States.checking_movie.set()


@dp.callback_query_handler(film_cd.filter(action="get movie by id"),
                           state=States.checking_movie)
async def query_get_movie_by_id(query: types.CallbackQuery):
    storage = await dp.storage.get_data(chat=query.from_user.id)
    id = query.data.split(":")[1]

    data = requests.get(Urls.get_full_data.format(
        id=id, imdb_token=IMDB_TOKEN)).json()

    if data['errorMessage']:
        await query.answer(Dialogs.error_message)
        return

    if data['plotLocal']:
        await query.message.edit_text(data['fullTitle'] + "\n" +
                                      data['plotLocal'],
                                      reply_markup=get_movie_info_keyboard(id))
    else:
        await query.message.edit_text(data['fullTitle'] + "\n" + data['plot'],
                                      reply_markup=get_movie_info_keyboard(id))

    storage['current_movie_data'] = MovieInfo(
        data['id'], data['fullTitle'], data['trailer']['linkEmbed'],
        data['posters']['posters'][:5], data['plot'], data['awards'],
        data['ratings'], data['stars'], data['similars'][:5],
        data['plotLocal'])

    await dp.storage.update_data(chat=query.from_user.id, data=storage)

    await States.checking_movie.set()


@dp.callback_query_handler(film_cd.filter(action="get trailer"),
                           state=States.checking_movie)
async def query_get_trailer(query: types.CallbackQuery):
    storage = await dp.storage.get_data(chat=query.from_user.id)

    id = storage['current_movie_data'].id

    await query.message.edit_text(storage['current_movie_data'].trailer_link,
                                  reply_markup=get_movie_info_keyboard(id))


@dp.callback_query_handler(film_cd.filter(action="get posters"),
                           state=States.checking_movie)
async def query_get_posters(query: types.CallbackQuery):
    storage = await dp.storage.get_data(chat=query.from_user.id)

    id = storage['current_movie_data'].id

    media = types.MediaGroup()

    for i in range(5):
        try:
            media.attach_photo(
                storage['current_movie_data'].get_poster_link(i), str(i))
        except:
            break

    await query.message.answer_media_group(media)
    await query.message.answer(Dialogs.get_posters_ok,
                               reply_markup=get_movie_info_keyboard(id))


@dp.callback_query_handler(film_cd.filter(action="get original plot"),
                           state=States.checking_movie)
async def query_get_original_plot(query: types.CallbackQuery):
    storage = await dp.storage.get_data(chat=query.from_user.id)

    await query.message.edit_text(storage['current_movie_data'].plot,
                                  reply_markup=get_movie_info_keyboard(id))


@dp.callback_query_handler(film_cd.filter(action="get local plot"),
                           state=States.checking_movie)
async def query_get_local_plot(query: types.CallbackQuery):
    storage = await dp.storage.get_data(chat=query.from_user.id)

    await query.message.edit_text(storage['current_movie_data'].plotLocal,
                                  reply_markup=get_movie_info_keyboard(id))


@dp.callback_query_handler(film_cd.filter(action="get stars"),
                           state=States.checking_movie)
async def query_get_stars(query: types.CallbackQuery):
    storage = await dp.storage.get_data(chat=query.from_user.id)

    id = storage['current_movie_data'].id

    await query.message.edit_text(storage['current_movie_data'].stars,
                                  reply_markup=get_movie_info_keyboard(id))


@dp.callback_query_handler(film_cd.filter(action="get ratings"),
                           state=States.checking_movie)
async def query_get_ratings(query: types.CallbackQuery):
    storage = await dp.storage.get_data(chat=query.from_user.id)

    id = storage['current_movie_data'].id

    await query.message.edit_text(storage['current_movie_data'].get_ratings(),
                                  reply_markup=get_movie_info_keyboard(id))


@dp.callback_query_handler(film_cd.filter(action="get rewards"),
                           state=States.checking_movie)
async def query_get_rewards(query: types.CallbackQuery):
    storage = await dp.storage.get_data(chat=query.from_user.id)

    id = storage['current_movie_data'].id

    await query.message.edit_text(storage['current_movie_data'].rewards,
                                  reply_markup=get_movie_info_keyboard(id))


@dp.callback_query_handler(film_cd.filter(action="get similars"),
                           state=States.checking_movie)
async def query_get_similars(query: types.CallbackQuery):
    storage = await dp.storage.get_data(chat=query.from_user.id)

    id = storage['current_movie_data'].id

    if len(storage['current_movie_data'].similars) == 0:
        await query.message.edit_text(Dialogs.error_no_similars,
                                      reply_markup=get_movie_info_keyboard(id))
        return

    media = types.MediaGroup()

    for i in range(len(storage['current_movie_data'].similars)):
        try:
            media.attach_photo(
                storage['current_movie_data'].similars_get_poster_link(i),
                str(i))
        except:
            break

    await query.message.answer_media_group(media)
    await query.message.answer(Dialogs.similars,
                               reply_markup=movies_list_keyboard(
                                   storage['current_movie_data'].similars))


@dp.callback_query_handler(film_cd.filter(action="add to favorite"),
                           state=States.checking_movie)
async def query_add_to_favorite(query: types.CallbackQuery):
    storage = await dp.storage.get_data(chat=query.from_user.id)

    id = storage['current_movie_data'].id

    try:
        requests.post(
            Urls.new_watch_item.format(
                api_uri=API_HOST,
                imdb_id=storage['current_movie_data'].id,
                user_id=query.from_user.id,
                title=storage['current_movie_data'].title))
        await query.message.edit_text(Dialogs.success_adding_movie,
                                      reply_markup=get_movie_info_keyboard(id))
    except:
        await query.message.edit_text(Dialogs.error_message,
                                      reply_markup=get_movie_info_keyboard(id))
        return


@dp.callback_query_handler(film_cd.filter(action="delete from favorite"),
                           state=States.checking_movie)
async def query_delete_from_favorite(query: types.CallbackQuery):
    storage = await dp.storage.get_data(chat=query.from_user.id)

    # Костыль чтобы получить id итема в закладках имея id пользователя и фильма
    movie_id = storage['current_movie_data'].id
    id = None
    data = requests.get(
        Urls.get_user_info.format(api_uri=API_HOST,
                                  id=query.from_user.id)).json()
    for i in data['info']['watch_item']:
        if i['imdb_id'] == movie_id:
            id = i['id']

    try:
        requests.delete(Urls.delete_watch_item.format(api_uri=API_HOST, id=id))
        await query.message.edit_text(
            Dialogs.success_deleting_movie,
            reply_markup=get_movie_info_keyboard(movie_id))
    except:
        await query.message.edit_text(
            Dialogs.error_message,
            reply_markup=get_movie_info_keyboard(movie_id))
        return


if __name__ == '__main__':
    executor.start_polling(dp)
