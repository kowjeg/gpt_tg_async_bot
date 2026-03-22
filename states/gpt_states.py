from aiogram.fsm.state import State, StatesGroup


class GPTStates(StatesGroup):
    gpt_chat = State()


class TalkingStates(StatesGroup):
    choosing_person = State()
    talking = State()


class QuizStates(StatesGroup):
    choosing_topic = State()
    waiting_answer = State()
    show_result = State()