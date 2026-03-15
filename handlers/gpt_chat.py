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

GPT_SYSTEM_PROMPT = 'Ты ИИ ассистент. Чат с пользователем. Ответы краткие. Ответ на том языке, на котором сообщение от пользователя.'
STATE_MESSAGE = '<b> Режим ChatGPT</b>\n\n Режим быстрой консультации по любым вопросам. Задай вопрос - я отвечу кратко и по делу. Для выхода из режима и возврата в меню - Кнопка <b>Завершить диалог</b>'

@router.message(Command('gpt'))
async def cmd_gpt(message: Message, state: FSMContext):
    await state.set_state(GPTStates.gpt_chat)
    await state.update_data(history= [])


    try:
        photo = FSInputFile('images/gpt.png')
        await message.answer_photo(photo=photo, caption=STATE_MESSAGE, reply_markup=gpt_chat_keyboard())


    except FileNotFoundError as e:

        logger.error('Файла картинки нет на диске!, %s', e)
        await message.answer(STATE_MESSAGE, reply_markup=gpt_chat_keyboard())

    except Exception as e:

        logger.error('Что-то не так с запросом к GPT, %s', e)
        await message.answer('Ошибка при взаимодействием с сервером GPT, попробуйте позже', reply_markup=gpt_chat_keyboard())


@router.message(GPTStates.gpt_chat, F.text)
async def gpt_message(message: Message, state: FSMContext):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )

    data = await state.get_data()
    user_message = message.text
    history = data.get('history', [])

    history.append({'role': 'user', 'content': user_message})

    try:
        response = await ask_gpt(user_message=user_message, system_prompt=GPT_SYSTEM_PROMPT, history=history[:-1])
    except Exception as e:
        logger.error('Что-то не так с запросом к GPT, %s', e)
        await message.answer('Ошибка при взаимодействием с сервером GPT, попробуйте позже',
                             reply_markup=gpt_chat_keyboard())
        return
    history.append({'role': 'assistant', 'content': response})
    if len(history) > 20:
        history = history[-20:]
        await state.update_data(history=history)

    await message.answer(response, reply_markup=gpt_chat_keyboard())


@router.callback_query(F.data == 'gpt:stop')
async def on_gpt_stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Выхожу из режима ChatGPT')
    await callback.message.delete()
    await callback.message.answer('Главное меню:\n\n', reply_markup=main_menu())
