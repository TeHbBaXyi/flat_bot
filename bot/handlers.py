from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import keyboards as kb
import sqlite3
from search import search

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
    await callback.message.answer("ХЗ ЧЕ ТЕ НЕ ПОНЯТНО",
                                      reply_markup=kb.back)

@router.callback_query(F.data == "main:filt")
async def filt(callback: CallbackQuery):
    await callback.message.answer("Выберите по чему будем фильтровать:",
                        reply_markup=kb.filters)
    await callback.answer()

@router.callback_query(F.data == "filter:pets")
async def question_pets(callback: CallbackQuery):
    await callback.message.answer("Вы с домашними животными?:",
                                  reply_markup=kb.pets)
    await callback.answer()
@router.callback_query(F.data.startswith("pets:"))
async def pets_yes_or_no(callback: CallbackQuery, state: FSMContext):
    pets = int(callback.data.split(":")[1])
    await state.update_data(pets_allowed=pets)
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
    await callback.message.answer("Введите максимульную стоимость аренды:",
                                      reply_markup=kb.back)
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
        await message.answer("Введите максимульную стоимость аренды:",
                                      reply_markup=kb.back)


@router.callback_query(F.data == "filter:district")
async def what_district(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Order.district)
    await callback.message.answer("Введите желаемые районы:",
                                      reply_markup=kb.back)
    await callback.answer()
@router.message(Order.district)
async def district(message: Message, state: FSMContext):
    words = message.text.replace(",", " ").split()
    conn = sqlite3.connect('flats.db')
    all_districts = {row[0] for row in conn.execute("SELECT DISTINCT district FROM appart")}
    conn.close()

    found = [w for w in words if w in all_districts]
    not_found = [w for w in words if w not in all_districts]

    if not found:
        await message.answer("Таких районов нет в списке!!!")
        await message.answer("Введите желаемые районы или нажмите «Назад»:", reply_markup=kb.back)
        return

    data = await state.get_data()
    old = data.get("district", [])
    new = old + [d for d in found if d not in old]
    await state.update_data(district=new)

    if not_found:
        await message.answer(f"Не нашёл районы: {', '.join(not_found)}")
        await message.answer(f"Сохранены районы: {', '.join(new)}")
        await message.answer("Можете ввести ещё районы или нажать «Назад»:", reply_markup=kb.back)
        return

    await state.set_state(None)
    await message.answer(f"Сохранены районы: {', '.join(new)}")
    await message.answer("Выберите по чему будем фильтровать:", reply_markup=kb.filters)


@router.callback_query(F.data == "filter:area")
async def what_area(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Order.area)
    await callback.message.answer("Введите минимальный размер квартиры:",
                                      reply_markup=kb.back)
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
        await message.answer("Введите минимальный размер квартиры:",
                                      reply_markup=kb.back)


@router.callback_query(F.data == "filter:metro")
async def what_metro(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Order.metro)
    await callback.message.answer("Введите желаемое метро:",
                                      reply_markup=kb.back)
    await callback.answer()
@router.message(Order.metro)
async def metro(message: Message, state: FSMContext):
    words = message.text.replace(",", " ").split()
    conn = sqlite3.connect('flats.db')
    all_metro = {row[0] for row in conn.execute("SELECT DISTINCT metro FROM appart")}
    conn.close()

    found = [w for w in words if w in all_metro]
    not_found = [w for w in words if w not in all_metro]

    if not found:
        await message.answer("Таких станций нет в списке!!!")
        await message.answer("Введите желаемые станции или нажмите «Назад»:", reply_markup=kb.back)
        return

    data = await state.get_data()
    old = data.get("metro", [])
    new = old + [m for m in found if m not in old]
    await state.update_data(metro=new)

    if not_found:
        await message.answer(f"Не нашёл станции: {', '.join(not_found)}")
        await message.answer(f"Сохранены станции: {', '.join(new)}")
        await message.answer("Можете ввести ещё станции или нажать «Назад»:", reply_markup=kb.back)
        return

    await state.set_state(None)
    await message.answer(f"Сохранены станции: {', '.join(new)}")
    await message.answer("Выберите по чему будем фильтровать:", reply_markup=kb.filters)


@router.callback_query(F.data == "filter:end")
async def end(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    final_res = search(**data)
    output_result = []
    for row in final_res:
        output_result.append(f"Цена {row[0]} руб, район {row[1]}, метро {row[2]}, комнат {row[3]}, квартира {row[4]} кв метра, "
              f"c животными {("можно" if row[5] == 1 else "нельзя")}")
    output_result = "\n".join(output_result)
    await callback.message.answer(output_result)


@router.callback_query(F.data == "back:1")
async def back(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await callback.message.answer("Выберите по чему будем фильтровать:",
                                  reply_markup=kb.filters)
    await callback.answer()