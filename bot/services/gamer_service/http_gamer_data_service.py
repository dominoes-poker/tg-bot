import asyncio
from typing import Any, Callable, Dict, Generator, Iterable, Optional, List
import aiohttp
from bot.services.gamer_service.gamer_data_service import GamerDataService, GamersLoaderType
from bot.services.httm_mixin import HTTPMixin
from bot.types.gamer import Gamer


def load_gamers(data: List[Dict]) -> Generator[Gamer, None, None]:
    return [load_gamer(gamer_data) for gamer_data in data]

def load_gamer(data: Dict) -> Gamer:
    return Gamer(
            id = data['id'],
            identificator = data['identificator'],
            name = data['name'],
        )

def gamer_to_dict(gamer: Gamer) -> Dict:
    return {
        'identificator': gamer.identificator,
        'name': gamer.name,
    }


class HTTPGamerDataService(GamerDataService, HTTPMixin):
    def __init__(self, data_service_url: str) -> None:
        super(HTTPMixin, self).__init__()
        self._data_service_url = data_service_url

    @property
    def gamer_api_url(self) -> str:
        return f'{self.api_url}/gamer'

    async def get_gamer(self, identificator: int, 
                        loader: GamersLoaderType = load_gamer) -> Optional[Gamer]:
        url = f'{self.gamer_api_url}/{identificator}'
        async with aiohttp.ClientSession() as session:
            try:
                result = await self.get(url, session)
            except aiohttp.client_exceptions.ClientResponseError as error:
                if error.code == 404:
                    return None
                
        return result.load(loader=loader)

    async def register(self, gamer: Gamer,
                       serializer: Callable[[Gamer], Dict]=gamer_to_dict,
                       loader: Callable[[Dict], Any]=load_gamer) -> Gamer:
        url = self.gamer_api_url
        body = serializer(gamer)
        async with aiohttp.ClientSession() as session:
            result = await self.post(url, body, session)
        return result.load(loader=loader)


    async def get_users(self, names: Iterable[str], 
                        loader: GamersLoaderType = load_gamers) -> List[Gamer]:
        url = f'{self.gamer_api_url}?name={",".join(name for name in names)}'
        async with aiohttp.ClientSession() as session:
            result = await self.get(url, session)
            return result.load(loader=loader)
        # return result.load(loader=loader)
