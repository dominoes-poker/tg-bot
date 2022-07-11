from database.session import SessionManager
from services.game_service.database_game_data_service import (
    DataBaseGameDataService, GameSerializer, RoundSerializer, StakeSerializer)
from services.game_service.game_data_service import GameDataService
from services.player_service.database_player_data_service import \
    PlayerSerializer


def get_game_data_service(session_manager: SessionManager) -> GameDataService:
    round_serializer = RoundSerializer(StakeSerializer())
    game_loader = GameSerializer(player_serializer=PlayerSerializer(), round_serializer=round_serializer)
    return DataBaseGameDataService(session_manager, game_loader)
