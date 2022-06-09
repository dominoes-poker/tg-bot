from aiogram.dispatcher.fsm.state import State, StatesGroup

class RootState(StatesGroup):
    TG_PLAYER_REGISTRATION = State()
    ON_HOLD                = State()
    GAME                   = State()

class TGPlayerRegisterState(StatesGroup):
    WHAT_USERNMAE_USE = State()
    WAIT_USERNAME   = State()

class NewPlayerRegisterState(StatesGroup):
    WAIT_USERNAME   = State()

class GameState(StatesGroup):
    WAIT_PLAYER_USERNAMES  = State()
