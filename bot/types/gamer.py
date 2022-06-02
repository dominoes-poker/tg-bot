from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Gamer:
    identificator: int
    name: str
    id: Optional[int] = None

@dataclass
class Game:
    owner: Gamer
    id: Optional[int] = None
    gamers: Optional[List[Gamer]] = None