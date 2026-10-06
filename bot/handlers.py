from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import keyboards as kb

class Order(StatesGroup):
    money = State()
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
