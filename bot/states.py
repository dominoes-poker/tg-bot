from aiogram.dispatcher.fsm.state import State, StatesGroup

class RootState(StatesGroup):
    TG_PLAYER_REGISTRATION = State()
    ON_HOLD                = State()
    GAME                   = State()

class TelegramPlayerRegisterState(StatesGroup):
    WHAT_USERNAME_USE = State()
    WAIT_USERNAME = State()

class ExternalPlayerRegisterState(StatesGroup):
    WAIT_USERNAME = State()

class GameState(StatesGroup):
    WAIT_PLAYER_USERNAMES = State()

class RoundState(StatesGroup):
    START = State()
    BRIBES = State()
    ON_HOLD = State()

class MakeBetsState(StatesGroup):
    USERNAME  = State()
    BET  = State()

class SetBribesState(StatesGroup):
    BRIBE = State()
