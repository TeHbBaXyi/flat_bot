from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Старт")]
])
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="фильтр")],
    [KeyboardButton(text="help")]
],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню")
filters = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Цена", callback_data="filter:price")],
    [InlineKeyboardButton(text="Комнаты", callback_data="filter:rooms")],
    [InlineKeyboardButton(text="Животные", callback_data="filter:pets")],
    [InlineKeyboardButton(text="Район", callback_data="filter:district")],
    [InlineKeyboardButton(text="Метро", callback_data="filter:metro")],
])