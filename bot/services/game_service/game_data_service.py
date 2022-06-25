from typing import Optional
from bot.services.loaders.game_loader import GameLoader
from bot.types import Game, Round, Stake
from bot.services.data_service import DataService


class GameDataService(DataService):

    async def get_game(self, identificator: Optional[int] = None,
                       loader: GameLoader= None) -> Optional[Game]:
        raise NotImplementedError

    async def create(self) -> Game:
        raise NotImplementedError

    async def start_new_round(self, round_: Round) -> Game:
        raise NotImplementedError

    async def set_bet(self, game_id: int, stake: Stake) -> Game:
        raise NotImplementedError

    async def set_bribe(self, game_id: int, stake: Stake) -> Game:
        raise NotImplementedError
