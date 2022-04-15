import logging

import dotenv
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from bot_dialogs_states import Dialogs, States
from keyboards import film_cd, get_main_keyboard, get_search_keyboard
from urls import Urls

# from aiogram.utils.exceptions import MessageNotModified, Throttled

config = dotenv.dotenv_values('.env')
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = config['TELEGRAM_TOKEN']
IMDB_TOKEN = config['IMDB_TOKEN']

storage = MemoryStorage()

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.callback_query_handler(film_cd.filter(action='get main page'), state="*")
async def query_main(query: types.InlineQuery, state: FSMContext):
    await query.message.edit_text(
        Dialogs.main_page.format(name=query.message.from_user.full_name),
        reply_markup=get_main_keyboard())

    if state:
        await state.finish()


@dp.message_handler(commands=['start', 'exit'], state="*")
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

    await message.answer(Dialogs.wait_loading)
    title = message.text
    data = requests.get(
        Urls.search_by_title.format(title=title,
                                    imdb_token=IMDB_TOKEN)).json()

    media = types.MediaGroup()
    for i in data['results'][:5]:
        media.attach_photo(i['image'], i['title'] + i['description'])

    await message.answer_media_group(media)

    text = Dialogs.get_movies_search_result
    for i, film in enumerate(data['results'][:5]):
        text += f"\n{i+1} {film['title']} {film['description']}"

    text += "\n\n"
    text += Dialogs.get_movies_get_number

    await message.answer(text=text, reply_markup=get_search_keyboard())

    storage = await dp.storage.get_data(chat=message.from_user.id, default={})

    storage['search_result'] = data['results'][:5]

    await dp.storage.update_data(chat=message.from_user.id, data=storage)

    await States.get_movie.set()


@dp.message_handler(state=States.get_movie)
async def state_get_movie(message: types.Message, state: FSMContext):
    storage = await dp.storage.get_data(chat=message.from_user.id)

    try:
        number = int(message.text) - 1
        id = storage['search_result'][number]['id']
        data = requests.get(Urls.get_by_id.format(
            id=id, imdb_token=IMDB_TOKEN)).json()

        #TODO - отдельная клавиатура сюда
        await message.answer(data['fullTitle'] + "\n" + data['plotLocal'])

        if state:
            await state.finish()
    except:
        await message.answer(Dialogs.get_movie_get_number_error)


# @dp.errors_handler(exception=MessageNotModified)
# async def message_not_modified_handler(update, error):
#     return True  # errors_handler must return True if error was handled correctly
if __name__ == '__main__':
    executor.start_polling(dp)
