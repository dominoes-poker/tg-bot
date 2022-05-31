
from dataclasses import dataclass
from typing import Optional


@dataclass
class Gamer:
    identificator: int
    name: str
    id: Optional[int] = None
