from typing import List, Optional
from bot.types import Player
from bot.services.data_service import DataService


class PlayerDataService(DataService):

    async def get_player(self, username: str) -> Optional[Player]:
        raise NotImplementedError

    async def register(self, player: Player) -> Player:
        raise NotImplementedError

    async def get_tg_player(self, identificator: List[str]) -> List[Player]:
        raise NotImplementedError
