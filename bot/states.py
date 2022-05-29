from aiogram.dispatcher.fsm.state import State, StatesGroup

class RootState(StatesGroup):
    GAMER_REGISTER = State()
    ON_HOLD = State()

class GamerRegisterState(StatesGroup):
    NAME = State()
    USERNAME = State()

    