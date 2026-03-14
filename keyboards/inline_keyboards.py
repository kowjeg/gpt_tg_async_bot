from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🎲Случайный факт', callback_data='btn:random', style='danger'),

            ],
            [
                InlineKeyboardButton(text='🤖Вопрос к ChatGPT', callback_data='btn:gpt', style='primary'),
            ],
            [
                InlineKeyboardButton(text='🧑‍🎤Диалог со знаменитостью', callback_data='btn:superstar'),
            ],
            [
                InlineKeyboardButton(text='🎯Quiz', callback_data='btn:quiz', style='success')
            ]
        ]
    )
    return keyboard

def rand_fact():
    return InlineKeyboardMarkup(
        inline_keyboard= [[InlineKeyboardButton(text='Ещё один факт', callback_data='btn:random',style='danger')]]
    )