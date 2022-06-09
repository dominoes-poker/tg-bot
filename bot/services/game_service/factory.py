from bot.services.game_service.http_game_data_service import HTTPGameDataService
from bot.services.game_service.game_data_service import GameDataService
from bot.services.loaders import GameLoader, PlayerLoader, RoundLoader


def get_game_data_service(data_service_url: str = 'http://127.0.0.1:3000') -> GameDataService:
    game_loader = GameLoader(player_loader=PlayerLoader(), round_loader=RoundLoader())
    return HTTPGameDataService(data_service_url=data_service_url, loader=game_loader)
