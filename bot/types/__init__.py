
from typing import Callable
from aiogram.dispatcher.fsm.context import FSMContext

from .message import IncommingMessage, IncommingMessageWrapper
from .gamer import Gamer


EventCallbackType = Callable[[IncommingMessage, FSMContext], None]
