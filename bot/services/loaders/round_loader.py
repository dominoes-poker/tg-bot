from typing import Dict, Any

from bot.services.loaders.loader import Loader
from bot.services.loaders.stake_loader import StakeLoader
from bot.types import Round


class RoundLoader(Loader):
    def __init__(self, stake_loader: StakeLoader):
        self._stake_loader = stake_loader
    
    def __call__(self, data: Dict[Any, Any]) -> Round:
        return Round(
            id=data['id'],
            numberOfDice=data['numberOfDice'],
            gameId=data['gameId'],
            number=data['number'],
            stakes=[self._stake_loader(stake) for stake in data['stakes']] if data['stakes'] else [],
        )