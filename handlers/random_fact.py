import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from services.openai_service import ask_gpt


logger = logging.getLogger(__name__)
router = Router()

RAND_FACT_PROMPT = 'Дай случайный интересный удивительный факт из любой области. Факт не длиннее трех средних предложений'


async def handle(callback: CallbackQuery):

    answer = await ask_gpt(RAND_FACT_PROMPT)

    try:
        file = FSInputFile('images/random.png')
    except FileNotFoundError as e:
        logger.error('Файла картинки нет на диске!, %s', e)
    await callback.message.answer_photo(photo=file, caption=f'<b>Случайный факт</b> \n\n {answer}' )

