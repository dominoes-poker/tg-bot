
from typing import List
import aiohttp
from bot.services.game_service.game_data_service import GameDataService
from bot.services.httm_mixin import HTTPMixin
from bot.services.loaders.game_loader import GameLoader
from bot.types import Player, Game, Round, Stake


def round_to_dict(round: Round) -> dict:
    return {
        'gameId': round.gameId,
        'numberOfDice':round.numberOfDice,
    }

def stake_to_dict(stake: Stake) -> dict:
    return {
        'playerId': stake.playerId,
        'bet':stake.bet,
    }

class HTTPGameDataService(GameDataService, HTTPMixin):
    def __init__(self, data_service_url: str, loader: GameLoader) -> None:
        super(HTTPGameDataService, self).__init__(loader)
        self._data_service_url = data_service_url

    @property
    def game_api_url(self) -> str:
        return f'{self.api_url}/game'

    async def create(self, players: List[Player]) -> Game:
        body = {'playerIds': [player.id for player in players]}
        async with aiohttp.ClientSession() as session:
            result = await self.post(self.game_api_url, body, session)
        return result.load(loader=self._loader)

    async def get_game(self, game_id: int) -> Game:
        url = f'{self.game_api_url}/{game_id}'
        async with aiohttp.ClientSession() as session:
            result = await self.get(url, session)
        return result.load(loader=self._loader)

    async def start_new_round(self, round: Round) -> Game:
        url = f'{self.game_api_url}/{round.gameId}/new-round'
        body = round_to_dict(round)
        async with aiohttp.ClientSession() as session:
            result = await self.post(url, body, session)
        return result.load(loader=self._loader.round_loader)
    
    async def player_makes_bet(self, game_id: int, stake: Stake) -> Game:
        url = f'{self.game_api_url}/{game_id}/round/{stake.roundId}/make-bet'
        body = stake_to_dict(stake)
        async with aiohttp.ClientSession() as session:
            result = await self.post(url, body, session)
        return result.load(loader=self._loader)


