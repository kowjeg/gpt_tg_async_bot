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
from keyboards.inline_keyboards import gpt_chat_keyboard, main_menu, person_keyboard, talking_keyboard

from json_storage.load_celebrities import CELEBRITIES


logger = logging.getLogger(__name__)
router = Router()
MAX_HISTORY_LENGTH = 20

async def cmd_talk(message: Message, state : FSMContext):
    await state.set_state(TalkingStates.choosing_person)
    await message.answer('Выбери персонажа для общения сегодня:\n\n', reply_markup=person_keyboard())



@router.callback_query(F.data == 'talk:stop')
@router.callback_query(F.data == 'talk:cancel')
async def on_talk_stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Выхожу из режима диалога')

    await callback.message.answer('Главное меню:\n\n', reply_markup=main_menu())
    await callback.message.delete()


@router.callback_query(F.data.startswith("talk:"))
async def handle_celebrity(callback: CallbackQuery, state: FSMContext):

    celebrity_key  = callback.data.split(":")[1]

    person = CELEBRITIES[celebrity_key]

    await state.set_state(TalkingStates.talking)
    await state.update_data(history=[], person=person)

    await callback.answer()
    await callback.message.answer(f'Начинаем разговор с {person['name']}\n\n Напишите что нибудь...',reply_markup=talking_keyboard())
    await callback.message.delete()



@router.message(TalkingStates.talking, F.text)
async def talking_handle(message: Message, state: FSMContext):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )

    data = await state.get_data()

    history = data.get('history', [])
    person = data.get('person')
    user_message = message.text

    try:
        response = await ask_gpt(user_message=user_message, system_prompt=person['description_prompt'], history=history)
    except Exception as e:
        logger.error('Что-то не так с запросом к GPT, %s', e)
        await message.answer('Ошибка при взаимодействием с сервером GPT, попробуйте позже',
                             reply_markup=talking_keyboard())
        return
    history.append({'role': 'user', 'content': user_message})
    history.append({'role': 'assistant', 'content': response})
    if len(history) > MAX_HISTORY_LENGTH:
        history = history[-MAX_HISTORY_LENGTH:]
    await state.update_data(history=history)

    await message.answer(response, reply_markup=talking_keyboard())