import random
import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from services.openai_service import ask_gpt
from keyboards.inline_keyboards import rand_fact

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


async def handle(callback: CallbackQuery):
    topic = random.choice(TOPICS)

    random_fact = f"Расскажи короткий удивительный факт про {topic}. Не более 3 предложений."

    answer = await ask_gpt(user_message=random_fact)

    try:
        file = FSInputFile('images/random.png')
    except FileNotFoundError as e:
        logger.error('Файла картинки нет на диске!, %s', e)
    await callback.message.answer_photo(photo=file, caption=f'<b>Случайный факт</b> \n\n {answer}', reply_markup=rand_fact())

