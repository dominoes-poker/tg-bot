from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.routers.utils import get_ending_for_ordered_number

BUTTON_YES = KeyboardButton(text='Yes')
BUTTON_NO = KeyboardButton(text='No')

KEYBOARD_YES_NO = ReplyKeyboardMarkup(
    keyboard=[[BUTTON_YES,BUTTON_NO]],
    resize_keyboard=True,
)

BUTTON_NEW_GAME = KeyboardButton(text='Start a new game')
BUTTON_ADD_GAMER = KeyboardButton(text='Register my frined')

KEYBOARD_ON_HOLD = ReplyKeyboardMarkup(
    keyboard=[[BUTTON_NEW_GAME],[BUTTON_ADD_GAMER]],
    resize_keyboard=True,
)

def keyboard_start_new_round(round_number: int) -> KeyboardButton:
    button_text = f'Start the {round_number}{get_ending_for_ordered_number(round_number)} round'
    buttons = [[
        KeyboardButton(text=button_text)
    ]]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )

def keyboard_from_data(data: List[str]) -> KeyboardButton:
    buttons = []
    for index, value in enumerate(data):
        button = KeyboardButton(text=value)
        if index % 2 == 0 :
            buttons.append([button])
        else:
            buttons[-1].append(button)
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )


BUTTON_ENTER_ROUND_RESULTS = KeyboardButton(text='Enter results for the round')

KEYBOARD_ENTER_ROUND_RESULTS = ReplyKeyboardMarkup(
    keyboard=[[BUTTON_ENTER_ROUND_RESULTS]],
    resize_keyboard=True,
)

BUTTON_SHOW_ROUND_STATISTICS = KeyboardButton(text='Show the round statistics')

KEYBOARD_SHOW_STATISTICS = ReplyKeyboardMarkup(
    keyboard=[[BUTTON_SHOW_ROUND_STATISTICS]],
    resize_keyboard=True,
)

BUTTON_SHOW_GAME_STATISTICS = KeyboardButton(text='Show the game statistics')

KEYBOARD_BEATWEEN_ROUNDS = ReplyKeyboardMarkup(
    keyboard=[
        [BUTTON_SHOW_ROUND_STATISTICS],
        [BUTTON_SHOW_GAME_STATISTICS]
        ],
    resize_keyboard=True,
)
