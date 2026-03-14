from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram.types import Message
from keyboards.inline_keyboards import main_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer('Привет! Тут можно узнать рандомный факт, '
                         'спросить что-то у ЧатГПТ, поговорить со знаменитостью '
                         'или поиграть в квиз:\n\n', reply_markup=main_menu())



