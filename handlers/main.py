import logging
from aiogram import Bot, Dispatcher, types
from button.buttons import *
from database.db import Database
import asyncio
import sqlite3
from aiogram.dispatcher.filters.state import StatesGroup, State

logging.basicConfig(level=logging.INFO)

API_TOKEN = '6706083284:AAGa85ZQXtVk37Cls6K_WwWylsrzpcnaeTM'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Инициализация базы данных
db = Database("bot_database.db")

class MyStates(StatesGroup):
    SomeState = State()

# storage = RedisStorage()
# dp = Dispatcher(bot, storage=storage)

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # Получаем информацию о пользователе
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Сохраняем информацию о пользователе в базе данных
    db.add_user(user_id, username, first_name, last_name)

    # Отправляем приветственное сообщение и кнопку "Далее"
    await message.answer("Привет! Я твой телеграм-бот!")
    await message.answer("Информация о боте:\n\n"
                         "Это пример телеграм-бота с использованием aiogram.\n\n"
                         "Нажми кнопку 'Далее', чтобы продолжить.", reply_markup=next_button)


# Обработка нажатия на кнопку 'Далее'
@dp.callback_query_handler(button_callback.filter(code='next'))
async def process_next_button(query: types.CallbackQuery):
    await query.answer("Вы нажали кнопку 'Далее'.")

    # Отправляем три кнопки "Тесты", "Экономика" и "Информация"
    await bot.send_message(query.from_user.id, "Выберите раздел:", reply_markup=get_main_menu_markup)


async def get_question_from_db(question_id=None):
    try:
        # Подключаемся к базе данных
        connection = sqlite3.connect("../bot_database.db")
        cursor = connection.cursor()

        # Выполняем SQL-запрос для получения вопроса
        cursor.execute("SELECT * FROM questions ORDER BY RANDOM()")
        question_id = cursor.fetchone()  # Получаем одну строку с таблицы

        # Закрываем соединение с базой данных
        connection.commit()

        return question_id

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return None, None


@dp.message_handler()
async def question(message: types.Message):
    if message.text == "Тесты":
        # Получаем вопрос и варианты ответа из базы данных
        question_row = await get_question_from_db()
        print(question_row)
        row_id, question_text, option1, option2, option3, option4, correct_option = question_row

        await message.answer_poll(
            question=question_text,
            options=[option1, option2, option3, option4],
            type='quiz',
            correct_option_id=correct_option,
            is_anonymous=False,
            open_period=10,
        )

    else:
        await message.answer("Ошибка при получении вопроса из базы данных.")
# async def question(message: types.Message, state: FSMContext):
#     if message.text == "Тесты":
#         # Получаем вопрос и варианты ответа из базы данных
#         question_row = await get_question_from_db()
#         print(question_row)
#         row_id, question_text, option1, option2, option3, option4, correct_option = question_row
#
#         # Сохраняем данные о вопросе в состоянии
#         await state.update_data(question_data={
#             'question_text': question_text,
#             'options': [option1, option2, option3, option4],
#             'correct_option': correct_option
#         })
#
#         await message.answer_poll(
#             question=question_text,
#             options=[option1, option2, option3, option4],
#             type='quiz',
#             correct_option_id=correct_option,
#             is_anonymous=False,
#             open_period=10,
#         )
#
#     else:
#         await message.answer("Ошибка при получении вопроса из базы данных.")




@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    question_row = await get_question_from_db()
    row_id, question_text, option1, option2, option3, option4, correct_option = question_row

    # correct_option=...

    # Если ответ правильный, увеличиваем рейтинг пользователя
    if quiz_answer.option_ids[0] == correct_option:
        db.increment_user_rating(quiz_answer.user.id)

# async def handle_poll_answer(quiz_answer: types.PollAnswer, state: FSMContext):
#     # Получаем данные о вопросе из состояния
#     data = await state.get_data(MyStates.SomeState.state)
#     correct_option = data['question_data']['correct_option']
#
#     # Если ответ правильный, увеличиваем рейтинг пользователя
#     if quiz_answer.option_ids[0] == correct_option:
#         db.increment_user_rating(quiz_answer.user.id)
#
#     # Сбрасываем состояние
#     await state.finish()



# Хендлер on_shutdown для удаления пользователя из базы данных при остановке бота
async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # Операции с базой данных в блоке with для гарантированного закрытия
    with db:
        pass  # Здесь можно добавить дополнительные операции перед закрытием базы данных

    # Завершаем выполнение асинхронного приложения
    await dp.storage.close()
    await dp.storage.wait_closed()

    # Закрываем базу данных после завершения работы бота
    db.close()


if __name__ == '__main__':
    from aiogram import executor
    try:
        executor.start_polling(dp, on_shutdown=on_shutdown, skip_updates=True)
    finally:
        asyncio.run(on_shutdown(dp) if dp.loop else on_shutdown(dp))


