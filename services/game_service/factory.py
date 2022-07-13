from database.session import SessionManager
from services.game_service.database_game_data_service import DataBaseGameDataService, GameSerializer
from services.game_service.game_data_service import GameDataService
from services.serializers import RoundSerializer, StakeSerializer, PlayerSerializer


def get_game_data_service(session_manager: SessionManager) -> GameDataService:
    round_serializer = RoundSerializer(StakeSerializer())
    player_serializer = PlayerSerializer()
    game_loader = GameSerializer(player_serializer=player_serializer, round_serializer=round_serializer)
    return DataBaseGameDataService(session_manager, game_loader)
