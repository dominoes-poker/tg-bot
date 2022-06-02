import asyncio
from typing import Any, Callable, Dict, Generator, Optional, List
import aiohttp
from bot.services.game_service.game_data_service import GameDataService
from bot.services.gamer_service.http_gamer_data_service import  load_gamers
from bot.services.httm_mixin import HTTPMixin
from bot.types.gamer import Gamer, Game


def load_game(data: Dict, owner: Optional[Gamer] = None) -> Game:
    return Game(
            id = data['id'],
            owner = owner,
            gamers = [owner]
        )


class HTTPGameDataService(GameDataService, HTTPMixin):
    def __init__(self, data_service_url: str) -> None:
        super(HTTPGameDataService, self).__init__()
        self._data_service_url = data_service_url

    @property
    def game_api_url(self) -> str:
        return f'{self.api_url}/game'


    async def create(self, gamer: Gamer,
                     loader: Callable[[Dict], Any]=load_game) -> Game:
        url = f'{self.game_api_url}'
        body = {'ownerId': gamer.id}
        async with aiohttp.ClientSession() as session:
            result = await self.post(url, body, session)
        return result.load(loader=lambda data: loader(data, owner=gamer))

    async def add_gamers(self, gamers: List[Gamer], game: Game,
                         loader: Callable[[Dict], Any]=load_game):
        url = f'{self.game_api_url}/{game.id}/add-gamers'
        body = {'gamerIds': [gamer.id for gamer in gamers]}        
        async with aiohttp.ClientSession() as session:
            result = await self.post(url, body, session)
        return result.load(loader=loader)

