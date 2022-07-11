
from typing import List
import aiohttp
from services.game_service.game_data_service import GameDataService
from services.httm_mixin import HTTPMixin
# from bot.services.loaders.game_loader import GameLoader
from bot.data_types import Player, Game, Round, Stake
GameLoader = None

def round_to_dict(round_: Round) -> dict:
    return {
        'gameId': round_.game_id,
        'numberOfDice':round_.number_of_dice,
    }

def stake_to_dict(stake: Stake) -> dict:
    return {
        'playerId': stake.player_id,
        'bet':stake.bet,
        'bribe':stake.bribe,
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

    async def start_new_round(self, round_: Round) -> Game:
        url = f'{self.game_api_url}/{round_.game_id}/new-round'
        body = round_to_dict(round_)
        async with aiohttp.ClientSession() as session:
            result = await self.post(url, body, session)
        return result.load(loader=self._loader.round_loader)

    async def set_bet(self, game_id: int, stake: Stake) -> Game:
        url = f'{self.game_api_url}/{game_id}/round/{stake.round_id}/bet'
        body = stake_to_dict(stake)
        async with aiohttp.ClientSession() as session:
            result = await self.post(url, body, session)
        return result.load(loader=self._loader)

    async def set_bribe(self, game_id: int, stake: Stake) -> Game:
        url = f'{self.game_api_url}/{game_id}/round/{stake["roundId"]}/bribe'

        async with aiohttp.ClientSession() as session:
            result = await self.post(url, stake, session)
        return result.load(loader=self._loader)

    async def finish(self, game_id: int) -> Game:
        url = f'{self.game_api_url}/{game_id}/finish'

        async with aiohttp.ClientSession() as session:
            result = await self.put(url, body=None, session=session)
        return result.load(loader=self._loader)