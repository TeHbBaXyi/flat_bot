from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Это бот по подбору арендного жилья.",
                         reply_markup=kb.main)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("ХЗ ЧЕ ТЕ НЕ ПОНЯТНО")

@router.message(F.text == "фильтр")
async def filt(message: Message):
    await message.answer("Выберите по чему будем фильтровать",
                        reply_markup=kb.filters)
