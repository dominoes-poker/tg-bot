
from dataclasses import dataclass
from typing import Optional


@dataclass
class Gamer:
    identificator: int
    username: str
    name: str
    id: Optional[int] = None
