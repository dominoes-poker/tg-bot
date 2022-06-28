from typing import List, Optional
from bot.types import Player
from bot.services.data_service import DataService


class PlayerDataService(DataService):
    async def register(self, player: Player) -> Player:
        raise NotImplementedError

    async def get_player_by_identificator(self, identificator: List[str]) -> List[Player]:
        raise NotImplementedError

    async def get_player_by_username(self, username: str) -> Optional[Player]:
        raise NotImplementedError

    async def get_players_by_username(self, usernames: List[str]) -> List[Player]:
        raise NotImplementedError
