import asyncio
from typing import Any, Callable, Dict, Generator, Optional, List
import aiohttp
from bot.services.game_service.game_data_service import GameDataService
from bot.services.httm_mixin import HTTPMixin
from bot.services.loaders.game_loader import GameLoader
from bot.types import Player, Game


class HTTPGameDataService(GameDataService, HTTPMixin):
    def __init__(self, data_service_url: str, loader: GameLoader) -> None:
        super(HTTPGameDataService, self).__init__(loader)
        self._data_service_url = data_service_url

    @property
    def game_api_url(self) -> str:
        return f'{self.api_url}/game'


    async def create(self, owner: Player) -> Game:
        url = f'{self.game_api_url}'
        body = {'ownerId': owner.id}
        async with aiohttp.ClientSession() as session:
            result = await self.post(url, body, session)
        return result.load(loader=self._loader)

    async def add_gamers(self, gamer_ids: List[int], game: Game) -> Game:
        url = f'{self.game_api_url}/{game.id}/add-gamers'
        body = {'gamerIds': gamer_ids}        
        async with aiohttp.ClientSession() as session:
            result = await self.post(url, body, session)
        return result.load(loader=self._loader)

