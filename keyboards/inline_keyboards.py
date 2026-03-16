from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from json_storage.load_celebrities import CELEBRITIES


def main_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🎲Случайный факт', callback_data='menu:random', style='primary'),

            ],
            [
                InlineKeyboardButton(text='🤖Вопрос к ChatGPT', callback_data='menu:gpt', style='primary'),
            ],
            [
                InlineKeyboardButton(text='🧑‍🎤Диалог со знаменитостью', callback_data='menu:talk', style='primary'),
            ],
            [
                InlineKeyboardButton(text='🎯Quiz', callback_data='menu:quiz', style='primary')
            ]
        ]
    )
    return keyboard


def rand_fact_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Ещё один факт', callback_data='random:again', style='success')],
            [InlineKeyboardButton(text='Закончить', callback_data='random:stop', style='danger')]
        ]
    )


def gpt_chat_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Закончить диалог', callback_data='gpt:stop', style='danger')]
        ]
    )


def talk_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=person["name"], callback_data=f'talk:{person["id"]}')
            ]
            for person in CELEBRITIES
        ]
    )