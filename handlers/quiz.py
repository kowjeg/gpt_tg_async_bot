import logging
from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext

from handlers.commands_handler import send_main_menu
from states.gpt_states import QuizStates
from services.openai_service import ask_gpt
from keyboards.inline_keyboards import  quiz_topic_keyboard, quiz_next_question, quiz_stop
from json_storage.load_files import TOPICS


logger = logging.getLogger(__name__)
router = Router()


async def cmd_quiz(message: Message, state : FSMContext):
    await state.set_state(QuizStates.choosing_topic)
    try:
        file = FSInputFile('images/quiz.png')
    except FileNotFoundError as e:
        logger.error('Файла картинки нет на диске!, %s', e)
    await message.answer_photo(photo=file, caption='Выбери тему квиза для игры:\n\n',
                                        reply_markup=quiz_topic_keyboard())


@router.callback_query(F.data == 'quiz:stop')
@router.callback_query(F.data == 'quiz:cancel')
async def on_quiz_stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Выхожу из режима Квиз')

    await send_main_menu(callback.message)
    await callback.message.delete()


@router.callback_query(QuizStates.choosing_topic, F.data.startswith("quiz:topic:"))
async def on_quiz_select_topic(callback: CallbackQuery, state: FSMContext):

    topic_key  = callback.data.split(":")[2]

    topic = TOPICS[topic_key]
    print(topic

          )
    await state.update_data(
        topic_key=topic_key,
        topic=topic,
        score={"correct": 0, "total": 0},
        current_question='',
        asked_questions=[]
    )

    await state.set_state(QuizStates.waiting_answer)
    await callback.message.edit_caption(
        caption=f'{topic} - отличный выбор! Генерирую вопрос'
    )

    await ask_question(callback.message, state)



async def ask_question(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    topic = data.get("topic", "general knowledge")
    score = data.get("score", {"correct": 0, "total": 0})
    asked_questions = data.get("asked_questions", [])

    history = []
    for q in asked_questions:
        history.append({"role": "assistant", "content": q})

    quiz_system_prompt = "Ты ведущий викторины. Генерируй уникальные вопросы по заданной теме. Никогда не повторяй уже заданные вопросы. Пиши только вопрос, без ответа. Кратко."
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )
    try:
        question = await ask_gpt(
            user_message=f"Придумай вопрос для викторины на тему: {topic}.",
            system_prompt=quiz_system_prompt,
            history=history or None
        )
        asked_questions.append(question)
        await state.update_data(current_question=question, asked_questions=asked_questions)
        await state.set_state(QuizStates.waiting_answer)

        score_text = (
            f"✅ {score['correct']} / {score['total']}"
            if score["total"] > 0
            else "Начинаем!"
        )
        
        await message.answer(f"📊 Счёт: {score_text}\n\n❓ {question}", reply_markup=quiz_stop())
    except Exception:
        await message.answer("⚠️ Ошибка генерации вопроса.")


@router.message(QuizStates.waiting_answer, F.text)
async def quiz_answer_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    question = data.get("current_question", "")

    prompt = (
        f"Вопрос: {question}\n"
        f"Ответ пользователя: {message.text}\n\n"
        "Правильный ли ответ? Ответь:\n"
        "1. '✅ Правильно!' или '❌ Неправильно!' на первой строке.\n"
        "2. Краткое объяснение (1-2 предложения) с правильным ответом."
    )
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )
    try:
        result = await ask_gpt(user_message=prompt)
    except Exception:
        await message.answer("⚠️ Ошибка проверки ответа.")
        return

    score: dict = data.get("score", {"correct": 0, "total": 0})
    score["total"] += 1
    if result.startswith("✅"):
        score["correct"] += 1

    await state.update_data(score=score)
    await state.set_state(QuizStates.show_result)

    await message.answer(
        f"{result}\n\n📊 Счёт: ✅ {score['correct']} / {score['total']}",
        reply_markup=quiz_next_question()
    )


@router.callback_query(QuizStates.show_result, F.data == "quiz:next")
async def quiz_next_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await ask_question(callback.message, state)


@router.callback_query(QuizStates.show_result, F.data == "quiz:end")
async def quiz_end_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    score = data.get("score", {"correct": 0, "total": 0})
    await state.clear()
    await callback.message.answer(
        f"🏁 Квиз завершён!\nФинальный счёт: ✅ {score['correct']} / {score['total']}"
    )
    await send_main_menu(callback.message)
