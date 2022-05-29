
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Gamer:
    id: Optional[int]
    identificator: int
    username: str
    name: str
