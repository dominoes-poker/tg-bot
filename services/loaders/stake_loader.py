from typing import Dict, Any

# from bot.services.loaders.loader import Loader
from bot.data_types import Stake


class StakeLoader:

    def __call__(self, data: Dict[Any, Any]) -> Stake:
        return Stake(
            id=data['id'],
            round_id=data['roundId'],
            player_id=data['playerId'],
            bet=data['bet'],
            bribe=data['bribe']
        )
