from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from src.keyboards import reply_keyboard, inline_keyboard


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Я твой первый бот.",
        reply_markup=reply_keyboard
    )
    print(f"Пользовтель {message.from_user.full_name}, с никнеймом {message.from_user.username} отправил команду /start")


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        "/start - приветствие\n"
        "/help - список команд",
        reply_markup=inline_keyboard
    )


@router.message(F.text == 'Каталог')
async def get_group(message: Message):
    await message.answer("Каталога нету!")


@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: CallbackQuery):
    await callback.answer("Начинаем игру!", show_alert=True)
    await callback.message.answer('Первый вопрос: Кто ты?')


@router.message(F.from_user.id == 1288365917)
async def get_group(message: Message):
    await message.answer("Привет мой создатель!!!!!")


@router.message()
async def echo(message: Message):
    if message.text == "Бектур":
        await message.answer("я поймал твое имя")
    else:
        await message.answer(f"Ты написал: {message.text}")