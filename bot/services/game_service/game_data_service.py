from typing import Callable, Dict, List, Optional
from bot.types.gamer import Game, Gamer
from bot.services.data_service import DataService

GamesLoaderType =  Callable[[Dict], List[Gamer]]

class GameDataService(DataService):

    async def get_game(self, identificator: Optional[int] = None, 
                       loader: GamesLoaderType = None) -> Optional[Gamer]:
        raise NotImplementedError

    async def create(self, gamer: Gamer):
        raise NotImplementedError

    async def add_gamers(self, gamers: List[Gamer], game: Game):
        raise NotImplementedError

