from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import keyboards as kb
import sqlite3


class Order(StatesGroup):
    money = State()
    district = State()
    metro = State()
    area = State()
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Это бот по подбору арендного жилья.",
                         reply_markup=kb.main)

@router.callback_query(F.data == "main:help")
async def help(callback: CallbackQuery):
    await callback.message.answer("ХЗ ЧЕ ТЕ НЕ ПОНЯТНО")

@router.callback_query(F.data == "main:filt")
async def filt(callback: CallbackQuery):
    await callback.message.answer("Выберите по чему будем фильтровать:",
                        reply_markup=kb.filters)
    await callback.answer()

@router.callback_query(F.data == "filter:pets")
async def question_pets(callback: CallbackQuery):
    await callback.message.answer("Выберите можно ли с животными:",
                                  reply_markup=kb.pets)
    await callback.answer()
@router.callback_query(F.data.startswith("pets:"))
async def pets_yes_or_no(callback: CallbackQuery, state: FSMContext):
    pets = int(callback.data.split(":")[1])
    await state.update_data(pets=pets)
    await callback.message.answer("Выберите по чему будем фильтровать:",
                                  reply_markup=kb.filters)

    data = await state.get_data()
    print(data)
    await callback.answer()


@router.callback_query(F.data == "filter:rooms")
async def how_many_rooms(callback: CallbackQuery):
    await callback.message.answer("Выберите сколько желаемое кол-во комнат:",
                                  reply_markup=kb.rooms)
    await callback.answer()
@router.callback_query(F.data.startswith("rooms:"))
async def quantity_rooms(callback: CallbackQuery, state: FSMContext):
    rooms = int(callback.data.split(":")[1])
    await state.update_data(rooms=rooms)
    await callback.message.answer("Выберите по чему будем фильтровать:",
                                  reply_markup=kb.filters)
    data = await state.get_data()
    print(data)
    await callback.answer()


@router.callback_query(F.data == "filter:price")
async def what_price(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Order.money)
    await callback.message.answer("Введите максимульную стоимость аренды:")
    await callback.answer()
@router.message(Order.money)
async def money(message: Message, state: FSMContext):
    try:
        price = int(message.text)
        await state.update_data(price=price)
        await state.set_state(None)
        data = await state.get_data()
        print(data)
        await message.answer("Выберите по чему будем фильтровать:",
                             reply_markup=kb.filters)
    except ValueError:
        await message.answer("Вы ввели не число!!!")
        await message.answer("Введите максимульную стоимость аренды:")


@router.callback_query(F.data == "filter:district")
async def what_district(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Order.district)
    await callback.message.answer("Введите желаемый район:")
    await callback.answer()
@router.message(Order.district)
async def district(message: Message, state: FSMContext):
    district = message.text.replace(",", " ").split(" ")
    conn = sqlite3.connect('flats.db')
    result_search = conn.execute("SELECT district FROM appart")
    all_districts = set()
    dist = []
    for row in result_search:
        all_districts.add(row[0])
    for word in district:
        if word in all_districts:
            dist.append(word)
    if len(dist) == 0:
        await message.answer("Такого района нет в списке!!!")
        await message.answer("Введите желаемый район:")
    else:
        await state.update_data(district=dist)
        await state.set_state(None)
        data = await state.get_data()
        print(data)
        await message.answer("Выберите по чему будем фильтровать:",
                             reply_markup=kb.filters)


@router.callback_query(F.data == "filter:area")
async def what_area(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Order.area)
    await callback.message.answer("Введите размер квартиры:")
    await callback.answer()
@router.message(Order.area)
async def area(message: Message, state: FSMContext):
    try:
        area = int(message.text)
        await state.update_data(area=area)
        await state.set_state(None)
        data = await state.get_data()
        print(data)
        await message.answer("Выберите по чему будем фильтровать:",
                             reply_markup=kb.filters)
    except ValueError:
        await message.answer("Вы ввели не число!!!")
        await message.answer("Введите размер квартиры:")


@router.callback_query(F.data == "filter:metro")
async def what_metro(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Order.metro)
    await callback.message.answer("Введите желаемое метро:")
    await callback.answer()
@router.message(Order.metro)
async def metro(message: Message, state: FSMContext):
    metro = message.text.replace(",", " ").split(" ")
    conn = sqlite3.connect('flats.db')
    result_search = conn.execute("SELECT metro FROM appart")
    all_metro = set()
    metro_result = []
    for row in result_search:
        all_metro.add(row[0])
    for word in metro:
        if word in all_metro:
            metro_result.append(word)
    if len(metro_result) == 0:
        await message.answer("Такого метро нет в списке!!!")
        await message.answer("Введите желаемое метро:")
    else:
        await state.update_data(metro=metro_result)
        await state.set_state(None)
        data = await state.get_data()
        print(data)
        await message.answer("Выберите по чему будем фильтровать:",
                             reply_markup=kb.filters)