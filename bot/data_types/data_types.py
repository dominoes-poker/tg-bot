
from typing import List, Optional
from attr import dataclass


@dataclass
class Stake:
    player_id: int
    round_id: int
    bet: Optional[int] = None
    bribe: Optional[int] = None
    id: Optional[int] = None


@dataclass
class Round:
    game_id: int
    number_of_dominoes: int
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
            return sorted(self.rounds, key=lambda round_: round_.number, reverse=True)[0]
        return None

    @property
    def max_round_number(self) -> int:
        return 17
