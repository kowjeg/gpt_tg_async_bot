import random
import logging
from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.filters import Command

from services.openai_service import ask_gpt
from keyboards.inline_keyboards import rand_fact_keyboard, main_menu

logger = logging.getLogger(__name__)
router = Router()


TOPICS = [
    "космос",
    "математика",
    "программирование",
    "древняя история",
    "психология",
    "технологии",
    "биология",
    "еда",
    "языки",
    "изобретения"
]


async def send_random_fact(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )
    topic = random.choice(TOPICS)

    random_fact = f"Расскажи короткий удивительный факт про {topic}. Не более 3 предложений."

    answer = await ask_gpt(user_message=random_fact)

    try:
        file = FSInputFile('images/random.png')
    except FileNotFoundError as e:
        logger.error('Файла картинки нет на диске!, %s', e)
    await message.answer_photo(photo=file, caption=f'<b>Случайный факт</b> \n\n {answer}',
                                        reply_markup=rand_fact_keyboard())


@router.message(Command('random'))
async def cmd_random(message: Message):
    await send_random_fact(message)

@router.callback_query(F.data == 'random:again')
async def query_random(callback : CallbackQuery):
    await send_random_fact(callback.message)
    await callback.answer()
    await callback.message.delete()

@router.callback_query(F.data == 'random:stop')
async def query_random_exit(callback : CallbackQuery):
    await callback.answer('Выхожу из режима RandomFact')
    await callback.message.delete()
    await callback.message.answer('Главное меню:\n\n', reply_markup=main_menu())





