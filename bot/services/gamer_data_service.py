from typing import Callable, Dict, List, Optional
from bot.types.gamer import Gamer
from bot.services.data_service import DataService

GamersLoaderType =  Callable[[Dict], List[Gamer]]

class GamerDataService(DataService):

    async def get_gmaer(self, identificator: int,
                        loader: GamersLoaderType) -> Optional[Gamer]:
        raise NotImplementedError

    async def register(self, gamer: Gamer):
        raise NotImplementedError
