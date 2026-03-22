from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram.types import Message, FSInputFile
from keyboards.inline_keyboards import main_menu
import logging

router = Router()
logger = logging.getLogger(__name__)

async def send_main_menu(message: Message) -> None:
    try:
        file = FSInputFile('images/menu.png')
    except FileNotFoundError as e:
        logger.error('Файла картинки нет на диске!, %s', e)
    await message.answer_photo(photo=file, caption='Привет! Тут можно узнать рандомный факт, '
                         'спросить что-то у ЧатГПТ, поговорить со знаменитостью '
                         'или поиграть в квиз:\n\n', reply_markup=main_menu())


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await send_main_menu(message)




