from aiogram.fsm.state import State, StatesGroup


class GPTStates(StatesGroup):
    gpt_chat = State()
    talk_superstar = State()
    random_fact = State()
    quiz = State()

