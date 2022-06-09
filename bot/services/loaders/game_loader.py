
from typing import Any, Dict
from bot.services.loaders.player_loader import PlayerLoader
from bot.services.loaders.loader import Loader
from bot.services.loaders.round_loader import RoundLoader
from bot.types import Game


class GameLoader(Loader):
    def __init__(self, player_loader: PlayerLoader, 
                       round_loader: RoundLoader):
        super().__init__()
        self._player_loader = player_loader
        self._round_loader = round_loader

    def __call__(self, data: Dict[Any, Any]) -> Game:
        return Game(
            id=data['id'],
            players=[self._player_loader(gamer_data) for gamer_data in data['players']],
            rounds=[self._round_loader(round_data) for round_data in data['rounds']],
            is_over=data['isOver']
        )