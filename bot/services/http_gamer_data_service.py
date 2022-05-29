from typing import Any, Callable, Dict, Generator, Optional
import aiohttp
from bot.services.gamer_data_service import GamerDataService
from bot.data_types.gamer import Gamer


def load_gamers(data: Dict) -> Generator[Gamer, None, None]:
    for gamer_data in data:
        yield Gamer(
            id = gamer_data['id'],
            identificator = gamer_data['identificator'],
            username = gamer_data['username'],
            name = gamer_data['name'],
        )


class RequestResult:
    def __init__(self, data: Dict[Any, Any]) -> None:
        self._data = data

    def load(self, loader: Callable[[Dict], Any]) -> Any:
        return loader(self._data['data'])


class HTTPGamerDataService(GamerDataService):
    def __init__(self, data_service_url: str) -> None:
        self._data_service_url = data_service_url
    
    @property
    def api_url(self) -> str:
        return f'{self._data_service_url}/api'

    @property
    def gamer_api_url(self) -> str:
        return f'{self.api_url}/gamer'
    
    async def get_gamer(self, identificator: int) -> Optional[Gamer]:
        url = f'{self.gamer_api_url}?identificator={identificator}'
        result = await self.get(url)
        gamers = result.load(loader=load_gamers)
        try:
            return next(gamers)
        except StopIteration:
            return None

    @staticmethod
    async def get(url: str) -> RequestResult:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, raise_for_status=True) as response:
                data = await response.json()
                return RequestResult(data)
