from database.session import SessionManager
from services.player_service.database_player_data_service import DataBasePlayerDataService, PlayerSerializer
from services.player_service.player_data_service import PlayerDataService

def get_player_data_service(session_manager: SessionManager) -> PlayerDataService:
    return DataBasePlayerDataService(serializer=PlayerSerializer(), session_manager=session_manager)
