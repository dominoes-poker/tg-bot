from typing import Dict, Any

from bot.services.loaders.loader import Loader
from bot.types import Stake


class StakeLoader(Loader):
    
    def __call__(self, data: Dict[Any, Any]) -> Stake:
        return Stake(
            id=data['id'],
            roundId=data['roundId'],
            playerId=data['playerId'],
            bet=data['bet']
        )