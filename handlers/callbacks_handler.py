import logging
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from handlers import random_fact, gpt_chat, talk


logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == 'menu:random')
async def handle_random_fact(callback: CallbackQuery):
    await random_fact.send_random_fact(callback.message)
    await callback.answer()
    await callback.message.delete()


@router.callback_query(F.data == 'menu:gpt')
async def handle_gpt_mode(callback: CallbackQuery, state: FSMContext):
    await gpt_chat.cmd_gpt(callback.message, state)
    await callback.answer()
    await callback.message.delete()



@router.callback_query(F.data == 'menu:talk')
async def handle_talk_menu(callback: CallbackQuery, state: FSMContext):
    await talk.cmd_talk(callback.message, state)
    await callback.answer()
    await callback.message.delete()
