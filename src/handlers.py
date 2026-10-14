from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.keyboards import reply_keyboard, inline_keyboard
from src.questions import QUESTIONS
from db.questions import get_all_questions, get_question
from db.results import get_score, save_result
from db.users import create_user, get_user


router = Router()


class Quiz(StatesGroup):
    waiting_answer = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.full_name or "Аноним"
    )
    await message.answer(
        f"Привет, {message.from_user.full_name}! Я твой первый бот.",
        reply_markup=reply_keyboard
    )
    print(f"Добавился новый пользователь {user}")


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        "/start - приветствие\n"
        "/help - список команд",
        reply_markup=inline_keyboard
    )


@router.message(Command('score'))
async def cmd_score(message: Message):
    user = get_user(telegram_id=message.from_user.id)
    if not user:
        await message.answer("Сначала нажми на /start")
    data = get_score(user["id"])
    await message.answer(f"Привет, твой результат:\nВсего вопросов: {data["total"]}\nИз них правильных: {data["correct"]}")


@router.callback_query(F.data == "score")
async def cmd_score(callback: CallbackQuery):
    await callback.answer()
    user = get_user(telegram_id=callback.from_user.id)

    if not user:
        await callback.message.answer("Сначала нажми на /start")
        return
    
    data = get_score(user["id"])
    await callback.message.answer(f"Привет, твой результат:\nВсего вопросов: {data["total"]}\nИз них правильных: {data["correct"]}")



@router.message(F.text == 'Каталог')
async def get_group(message: Message):
    await message.answer("Каталога нету!")

# Старт нашей викторины по кнопке
@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Начинаем игру!", show_alert=True)
    questions = get_all_questions()
    if not questions:
        await callback.message.answer("Вопросов нету!")
        return 
    await state.update_data(questions=questions, index=0, score=0)       # сохраняем процесс
    await state.set_state(Quiz.waiting_answer)       # переходим в состояние
    await callback.message.answer(f'Вопрос 1: {questions[0]["question_text"]}')


# Принимаем ответ - хендлер сработает ТОЛЬКО в состоянии waiting_answer
@router.message(Quiz.waiting_answer)
async def habdle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    questions = data["questions"]
    index = data["index"]
    score = data["score"]
    user = get_user(telegram_id=message.from_user.id)
    q = questions[index]

    is_correct = message.text.lower() == q["correct_answer"]
    save_result(
        user_id=user["id"],
        question_id=q["id"],
        is_correct=is_correct
    )

    if is_correct:
        score += 1
        await message.answer("Правильно: +1")
    else:
        await message.answer(f"Неверно. Правльный ответ: {q["correct_answer"]}")

    index += 1
    if index >= len(questions):
        await message.answer(f"Конец! Счет: {score}/{len(questions)}")
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f"Вопрос {index + 1}: {questions[index]["question_text"]}")


@router.message(F.from_user.id == 1288365917)
async def get_group(message: Message):
    await message.answer("Привет мой создатель!!!!!")


@router.message()
async def echo(message: Message):
    if message.text == "Бектур":
        await message.answer("я поймал твое имя")
    else:
        await message.answer(f"Ты написал: {message.text}")