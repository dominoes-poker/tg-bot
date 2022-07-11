from typing import List

from services.data_service import DataService
from bot.data_types import Game, Player, Round, Stake


class GameDataService(DataService):

    async def get_game(self, game_id: int) -> Game:
        raise NotImplementedError

    async def create(self, players: List[Player]) -> Game:
        raise NotImplementedError

    async def start_new_round(self, round_: Round) -> Game:
        raise NotImplementedError

    async def set_bet(self, game_id: int, stake: Stake) -> Game:
        raise NotImplementedError

    async def set_bribe(self, game_id: int, stake: Stake) -> Game:
        raise NotImplementedError

    async def finish(self, game_id: int) -> Game:
        raise NotImplementedError
