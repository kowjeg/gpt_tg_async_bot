import logging
import json
from aiogram import F, Router
import json_storage
from aiogram.enums import ChatAction
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.gpt_states import GPTStates, TalkingStates
from services.openai_service import ask_gpt
from keyboards.inline_keyboards import gpt_chat_keyboard, main_menu, talk_keyboard

from json_storage.load_celebrities import CELEBRITIES


logger = logging.getLogger(__name__)
router = Router()


async def cmd_talk(message: Message, state : FSMContext):
    await state.set_state(TalkingStates.choosing_person)
    await message.answer('Выбери персонажа для общения сегодня:\n\n', reply_markup=talk_keyboard())



@router.callback_query(F.data.startswith("talk:"))
async def handle_celebrity(callback: CallbackQuery, state: FSMContext):

    celebrity_id = callback.data.split(":")[1]



    await callback.answer()
    await callback.message.delete()
