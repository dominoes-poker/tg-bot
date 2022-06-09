from typing import Callable, Dict, List, Optional
from bot.types import Game, Player
from bot.services.data_service import DataService

GamesLoaderType =  Callable[[Dict], List[Player]]

class GameDataService(DataService):

    async def get_game(self, identificator: Optional[int] = None, 
                       loader: GamesLoaderType = None) -> Optional[Player]:
        raise NotImplementedError

    async def create(self):
        raise NotImplementedError

    async def add_gamers(self, gamer_ids: List[int], game: Game):
        raise NotImplementedError

