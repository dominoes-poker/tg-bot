
from typing import List, Optional
from attr import dataclass

from .message import IncommingMessage, IncommingMessageWrapper, ReplyMarkupType, ReplyKeyboardRemove

@dataclass
class Stake:
    playerId: int
    roundId: int
    bet: int
    bribe: Optional[int] = None
    id: Optional[int] = None


@dataclass
class Round:
    gameId: int
    numberOfDice: int
    stakes: Optional[List[Stake]] = None
    number: Optional[int] = None
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

    @property
    def last_round(self) -> Optional[Round]:
        if self.rounds:
            return sorted(self.rounds, key=lambda round: round.number, reverse=True)[0]
        return None
