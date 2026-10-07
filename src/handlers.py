from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.keyboards import reply_keyboard, inline_keyboard
from src.questions import QUESTIONS


router = Router()


class Quiz(StatesGroup):
    waiting_answer = State()


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

# Старт нашей викторины по кнопке
@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Начинаем игру!", show_alert=True)
    await state.update_data(index=0, score=0)       # сохраняем процесс
    await state.set_state(Quiz.waiting_answer)       # переходим в состояние
    await callback.message.answer(f'Вопрос 1: {QUESTIONS[0]['q']}')


# Принимаем ответ - хендлер сработает ТОЛЬКО в состоянии waiting_answer
@router.message(Quiz.waiting_answer)
async def habdle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    score = data["score"]

    if message.text.lower() == QUESTIONS[index]['a']:
        score += 1
        await message.answer("Правильно: +1")
    else:
        await message.answer(f"Неверно. Правльный ответ: {QUESTIONS[index]['a']}")

    index += 1
    if index >= len(QUESTIONS):
        await message.answer(f"Конец! Счет: {score}/{len(QUESTIONS)}")
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f"Вопрос {index + 1}: {QUESTIONS[index]['q']}")


@router.message(F.from_user.id == 1288365917)
async def get_group(message: Message):
    await message.answer("Привет мой создатель!!!!!")


@router.message()
async def echo(message: Message):
    if message.text == "Бектур":
        await message.answer("я поймал твое имя")
    else:
        await message.answer(f"Ты написал: {message.text}")