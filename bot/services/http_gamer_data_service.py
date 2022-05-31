from typing import Any, Callable, Dict, Generator, Optional, List
import aiohttp
from bot.services.gamer_data_service import GamerDataService, GamersLoaderType
from bot.types.gamer import Gamer


def load_gamers(data: List[Dict]) -> Generator[Gamer, None, None]:
    return (load_gamer(gamer_data) for gamer_data in data)

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

class RequestResult:
    def __init__(self, data: Dict[Any, Any]) -> None:
        self._data = data


    def load(self, loader: Callable[[Dict], Any]) -> Any:
        return loader(self._data['data'])


class HTTPGamerDataService(GamerDataService):
    def __init__(self, data_service_url: str) -> None:
        super().__init__()
        self._data_service_url = data_service_url

    @property
    def api_url(self) -> str:
        return f'{self._data_service_url}/api'

    @property
    def gamer_api_url(self) -> str:
        return f'{self.api_url}/gamer'

    async def get_gamer(self, identificator: int,
                        loader: GamersLoaderType = load_gamers) -> Optional[Gamer]:
        url = f'{self.gamer_api_url}?identificator={identificator}'
        result = await self.get(url)
        gamers = result.load(loader=loader)
        try:
            return next(gamers)
        except StopIteration:
            return None

    async def register(self, gamer: Gamer,
                       serializer: Callable[[Gamer], Dict]=gamer_to_dict,
                       loader: Callable[[Dict], Any]=load_gamer) -> Gamer:
        url = self.gamer_api_url
        body = serializer(gamer)
        result = await self.post(url, body)
        return result.load(loader=loader)

    @staticmethod
    async def get(url: str) -> RequestResult:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, raise_for_status=True) as response:
                data = await response.json()
                return RequestResult(data)

    @staticmethod
    async def post(url: str, body: Dict) -> RequestResult:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=body, raise_for_status=True) as response:
                data = await response.json()
                return RequestResult(data)
