import logging
from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.gpt_states import GPTStates
from services.openai_service import ask_gpt
from keyboards.inline_keyboards import gpt_chat_keyboard, main_menu


logger = logging.getLogger(__name__)
router = Router()


PERSONS = {

}