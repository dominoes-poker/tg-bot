import asyncio
from itertools import chain
from typing import Any, Callable, Dict, Iterable, Optional, List
import aiohttp
from bot.services.player_service.player_data_service import PlayerDataService
from bot.services.httm_mixin import HTTPMixin
from bot.services.loaders import PlayerLoader
from bot.types import Player


def player_to_dict(player: Player) -> Dict:
    return {
        'identificator': player.identificator,
        'username': player.username,
    }

class HTTPPlayerDataService(PlayerDataService, HTTPMixin):
    def __init__(self, data_service_url: str, loader: PlayerLoader) -> None:
        super(PlayerDataService, self).__init__(loader)
        self._data_service_url = data_service_url

    @property
    def _player_api_url(self) -> str:
        return f'{self.api_url}/player'

    def _get_url_for_request_by_username(self, username) -> str:
        return f'{self._player_api_url}?username={username}'

    async def register(self, player: Player,
                       serializer: Callable[[Player], Dict]=player_to_dict) -> Player:
        url = self._player_api_url
        body = serializer(player)
        async with aiohttp.ClientSession() as session:
            result = await self.post(url, body, session)
        return result.load(loader=self._loader)

    async def get_player_by_identificator(self, identificator: Iterable[str]) -> List[Player]:
        url = f'{self._player_api_url}?identificator={identificator}'
        async with aiohttp.ClientSession() as session:
            result = await self.get(url, session)
        players = result.load(loader=lambda data: [self._loader(user_data) for user_data in data])
        if len(players) == 1:
            return players[0]
        return None

    async def get_player_by_username(self, username: str) -> Optional[Player]:
        url = self._get_url_for_request_by_username(username)
        async with aiohttp.ClientSession() as session:
            try:
                result = await self.get(url, session)
            except aiohttp.client_exceptions.ClientResponseError as error:
                if error.code == 404:
                    return None
        return result.load(loader=self._loader)
    
    async def get_players_by_username(self, usernames: List[str]) -> List[Player]:
        urls = [self._get_url_for_request_by_username(username) for username in usernames]
        async with aiohttp.ClientSession() as session:
            requests = [self.get(url, session, raise_for_status=False) for url in urls]
            results = await asyncio.gather(*requests)
        players = [
            result.load(loader=lambda data: [self._loader(user_data) for user_data in data])
            for result in results
        ]
        return list(chain.from_iterable(players))
