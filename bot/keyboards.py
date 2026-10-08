from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Старт")]
])
main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Фильтр", callback_data="main:filt")],
    [InlineKeyboardButton(text="Помощь", callback_data="main:help")]
])
filters = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Цена", callback_data="filter:price")],
    [InlineKeyboardButton(text="Кол-во комнат", callback_data="filter:rooms")],
    [InlineKeyboardButton(text="Животные", callback_data="filter:pets")],
    [InlineKeyboardButton(text="Район", callback_data="filter:district")],
    [InlineKeyboardButton(text="Метро", callback_data="filter:metro")],
    [InlineKeyboardButton(text="Размер квартиры", callback_data="filter:area")],
    [InlineKeyboardButton(text="РЕЗУЛЬТАТ ПОИСКА", callback_data="filter:end")]
])
pets = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="pets:1")],
    [InlineKeyboardButton(text="Нет", callback_data="pets:0")],
    [InlineKeyboardButton(text="Назад", callback_data="back:1")]
])
rooms = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1", callback_data="rooms:1")],
    [InlineKeyboardButton(text="2", callback_data="rooms:2")],
    [InlineKeyboardButton(text="3", callback_data="rooms:3")],
    [InlineKeyboardButton(text="Назад", callback_data="back:1")]
])
back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back:1")],
])
def more(offset):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать еще", callback_data=f"more:{offset}")],
        [InlineKeyboardButton(text="Назад", callback_data="back:1")]
    ])
