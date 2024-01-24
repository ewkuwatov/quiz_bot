from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_callback = CallbackData("button", "code")
menu_callback = CallbackData("menu", "action")

# Создаем клавиатуру с кнопками
next_button = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="Далее", callback_data=button_callback.new(code="next")),
                                        ],
                                    ])

# Функция для получения Reply-кнопок "Тесты", "Экономика" и "Информация"
get_main_menu_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Тесты"),
                KeyboardButton(text="Экономика"),
                KeyboardButton(text="Информация"),
            ],
        ],
        resize_keyboard=True,
    )


