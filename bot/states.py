from aiogram.dispatcher.fsm.state import State, StatesGroup

class RootState(StatesGroup):
    GAMER_REGISTER = State()
    ON_HOLD = State()
    GAME = State()

class GamerRegisterState(StatesGroup):
    WAIT_USERNAME = State()

class GameState(StatesGroup):
    ADD_GAMERS = State()
    WAIT_GAMER_NAMES = State()
    WAIT_ANSWER = State()
