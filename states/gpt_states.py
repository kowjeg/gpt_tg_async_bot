from aiogram.fsm.state import State, StatesGroup


class GPTStates(StatesGroup):
    gpt_chat = State()
    talk_superstar = State()
    quiz = State()

