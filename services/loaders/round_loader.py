from typing import Dict, Any

# from services.loaders.loader import Loader
# from bot.services.loaders.stake_loader import StakeLoader
from bot.data_types import Round


class RoundLoader:
    def __init__(self, stake_loader):
        super().__init__()
        self._stake_loader = stake_loader

    def __call__(self, data: Dict[Any, Any]) -> Round:
        return Round(
            id=data['id'],
            number_of_dice=data['numberOfDice'],
            game_id=data['gameId'],
            number=data['number'],
            stakes=[
                    self._stake_loader(stake) for stake in data['stakes']
                ] if data['stakes'] else [],
        )
