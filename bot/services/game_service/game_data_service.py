from typing import Callable, Dict, List, Optional
from bot.services.loaders.game_loader import GameLoader
from bot.types import Game, Player
from bot.services.data_service import DataService


class GameDataService(DataService):

    async def get_game(self, identificator: Optional[int] = None, 
                       loader: GameLoader= None) -> Optional[Player]:
        raise NotImplementedError

    async def create(self) -> Game:
        raise NotImplementedError    
    
    async def start_new_round(self, game_id: int) -> Game:
        raise NotImplementedError


