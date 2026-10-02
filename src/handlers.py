from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Я твой первый бот."
    )
    print(f"Пользовтель {message.from_user.full_name}, с никнеймом {message.from_user.username} отправил команду /start")


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        "/start - приветствие\n"
        "/help - список команд"
    )


@router.message(F.text.lower() == 'группа')
async def get_group(message: Message):
    await message.answer("Твоя группа 70-2")


@router.message(F.from_user.id == 1288365917)
async def get_group(message: Message):
    await message.answer("Привет мой создатель!!!!!")


@router.message()
async def echo(message: Message):
    if message.text == "Бектур":
        await message.answer("я поймал твое имя")
    else:
        await message.answer(f"Ты написал: {message.text}")