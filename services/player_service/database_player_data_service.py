from typing import List, Optional, Union, Iterable

from sqlalchemy import select, exc

from bot.data_types import Player
from bot.errors.factories import create_db_player_error

from database.models import Player as DBPlayer
from database.session import SessionManager
from services.database_mixin import DatabaseMixin

from services.player_service.player_data_service import PlayerDataService
from services.serializers import Serializer


class DataBasePlayerDataService(PlayerDataService, DatabaseMixin):
    def __init__(self, serializer: Serializer, session_manager: SessionManager) -> None:
        PlayerDataService.__init__(self, serializer=serializer)
        DatabaseMixin.__init__(self, session_manager=session_manager)

    async def register(self, player: Player) -> Player:
        db_player = self._serializer.serialize(player)
        try:
            async with self._session_manager.session() as session:
                async with session.begin():
                    session.add_all([db_player])
        except exc.IntegrityError as error:
            raise create_db_player_error(error)
        return self._serializer.deserialize(db_player)

    async def get_player_by_identificator(self, identificator: Union[str, int]) -> List[Player]:
        query = select(DBPlayer).where(DBPlayer.identificator == str(identificator))
        return await self.first(query)

    async def get_player_by_username(self, username: str) -> Optional[Player]:
        query = select(DBPlayer).where(DBPlayer.username == username)
        return await self.first(query)
    
    async def get_players_by_username(self, usernames: Iterable[str]) -> List[Player]:
        query = select(DBPlayer).where(DBPlayer.username.in_(list(usernames)))
        return await self.all(query)
