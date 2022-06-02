from typing import Any, Callable, Dict
import aiohttp


class RequestResult:
    def __init__(self, data: Dict[Any, Any]) -> None:
        self._data = data


    def load(self, loader: Callable[[Dict], Any]) -> Any:
        return loader(self._data['data'])


class HTTPMixin:
    def __init__(self, data_service_url: str) -> None:
        super().__init__()
        self._data_service_url = data_service_url

    @property
    def api_url(self) -> str:
        return f'{self._data_service_url}/api'

    @staticmethod
    async def get(url: str, session: aiohttp.ClientSession) -> RequestResult:
        async with session.get(url, raise_for_status=True) as response:
            data = await response.json()
            return RequestResult(data)

    @staticmethod
    async def post(url: str, body: Dict[str, Any], session: aiohttp.ClientSession) -> RequestResult:
        async with session.post(url, data=body, raise_for_status=True) as response:
            data = await response.json()
            return RequestResult(data)
