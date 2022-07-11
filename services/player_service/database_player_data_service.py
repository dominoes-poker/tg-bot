from typing import List, Optional, Union

from sqlalchemy import select

from bot.data_types import Player

from database.models import Player as DBPlayer
from database.session import SessionManager
from services.database_mixin import DatabaseMixin

from services.player_service.player_data_service import PlayerDataService
from services.serializer import Serializer


class PlayerSerializer(Serializer):
    @staticmethod
    def convert(player, to_type):
        result = to_type(
            username=player.username,
            identificator=str(player.identificator)
        )
        if player.id is not None:
            result.id = id
        return result

    def serialize(self, player: Player) -> DBPlayer:
        return DBPlayer(
            username=player.username,
            identificator=str(player.identificator)
        )
    
    def deserialize(self, player: DBPlayer) -> Optional[Player]:
        if not player:
            return None
        return Player(
            id=player.id,
            username=player.username,
            identificator=player.identificator
        )


class DataBasePlayerDataService(PlayerDataService, DatabaseMixin):
    def __init__(self, serializer: Serializer, session_manager: SessionManager) -> None:
        PlayerDataService.__init__(self, serializer=serializer)
        DatabaseMixin.__init__(self, session_manager=session_manager)

    async def register(self, player: Player) -> Player:
        db_player = self._serializer.serialize(player)
        async with self._session_manager.session() as session:
            async with session.begin():
                session.add_all([
                    db_player
                ])
        
        return self._serializer.deserialize(db_player)

    async def get_player_by_identificator(self, identificator: Union[str, int]) -> List[Player]:
        query = select(DBPlayer).where(DBPlayer.identificator == str(identificator))
        return await self.first(query)

    async def get_player_by_username(self, username: str) -> Optional[Player]:
        query = select(DBPlayer).where(DBPlayer.username == username)
        return await self.first(query)
    
    async def get_players_by_username(self, usernames: List[str]) -> List[Player]:
        query = select(DBPlayer).where(DBPlayer.username.in_(usernames))
        return await self.all(query)
