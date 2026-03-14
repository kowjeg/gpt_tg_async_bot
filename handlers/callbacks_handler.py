import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery
from handlers import random_fact

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == 'btn:random')
async def handle_random_fact(callback: CallbackQuery):

    await random_fact.handle(callback)
    await callback.answer()

