from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BUTTON_YES = KeyboardButton(text='Yes')
BUTTON_NO = KeyboardButton(text='No')

YES_NO_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[BUTTON_YES,BUTTON_NO]],
    resize_keyboard=True,
)

BUTTON_NEW_GAME = KeyboardButton(text='Start a new game')
BUTTON_SHOW_STATISTICS = KeyboardButton(text='Show statistics')

ON_HOLD_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[BUTTON_NEW_GAME],[BUTTON_SHOW_STATISTICS]],
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