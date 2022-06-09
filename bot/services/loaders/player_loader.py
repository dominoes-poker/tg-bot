from typing import Dict, Any

from bot.services.loaders.loader import Loader
from bot.types import Player


class PlayerLoader(Loader):
    
    def __call__(self, data: Dict[Any, Any]) -> Any:
        return Player(
            id=data['id'],
            username=data['username']
        )