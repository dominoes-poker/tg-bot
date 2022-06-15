from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BUTTON_YES = KeyboardButton(text='Yes')
BUTTON_NO = KeyboardButton(text='No')

YES_NO_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[BUTTON_YES,BUTTON_NO]],
    resize_keyboard=True,
)

BUTTON_NEW_GAME = KeyboardButton(text='Start a new game')
BUTTON_ADD_GAMER = KeyboardButton(text='Register my frined')

ON_HOLD_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[BUTTON_NEW_GAME],[BUTTON_ADD_GAMER]],
    resize_keyboard=True,
)

def keyboard_round(round_number: int) -> KeyboardButton:
    number_to_text = (
        'first', 'second'
    )
    button_text = f'Start the {number_to_text[round_number-1]} round'
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

ENTER_ROUND_RESULTS_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[BUTTON_ENTER_ROUND_RESULTS]],
    resize_keyboard=True,
)

SHOW_STATISTICS_BUTTON = KeyboardButton(text='Show Statistics')

SHOW_STATISTICS_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[SHOW_STATISTICS_BUTTON]],
    resize_keyboard=True,
)