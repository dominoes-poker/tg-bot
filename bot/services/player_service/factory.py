from bot.services.player_service.http_player_data_service import HTTPPlayerDataService
from bot.services.player_service.player_data_service import PlayerDataService
from bot.services.loaders import PlayerLoader


def get_player_data_service(data_service_url: str = 'http://127.0.0.1:3000') -> PlayerDataService:
    return HTTPPlayerDataService(data_service_url=data_service_url, loader=PlayerLoader())
