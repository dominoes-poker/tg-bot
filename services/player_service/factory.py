from database.session import SessionManager
from services.player_service.database_player_data_service import DataBasePlayerDataService
from services.player_service.player_data_service import PlayerDataService
from services.serializers import PlayerSerializer


def get_player_data_service(session_manager: SessionManager) -> PlayerDataService:
    player_serializer = PlayerSerializer()
    return DataBasePlayerDataService(
        serializer=player_serializer,
        session_manager=session_manager
    )
