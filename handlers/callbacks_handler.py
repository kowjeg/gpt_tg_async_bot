import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery
from handlers import random_fact


logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == 'menu:random')
async def handle_random_fact(callback: CallbackQuery):
    await random_fact.send_random_fact(callback.message)
    await callback.answer()
    await callback.message.delete()


@router.callback_query(F.data == 'menu:gpt')
async def handle_random_fact(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer('Напиши /gpt чтобы войти в режим ChatGPT')


