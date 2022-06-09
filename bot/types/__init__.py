
from typing import Callable, List, Optional
from aiogram.dispatcher.fsm.context import FSMContext
from attr import dataclass

from .message import IncommingMessage, IncommingMessageWrapper


@dataclass
class Round:
    id: Optional[int] = None


@dataclass
class Player:
    username:      str
    identificator: Optional[str] = None
    id:            Optional[int] = None

@dataclass
class Game:
    is_over: bool
    id:      Optional[int] = None
    players: List[Player] = None
    rounds:  List[Round] = None

