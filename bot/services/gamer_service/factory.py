from bot.services.gamer_service.http_gamer_data_service import HTTPGamerDataService
from bot.services.gamer_service.gamer_data_service import GamerDataService


def get_gamer_data_service(data_service_url: str = 'http://127.0.0.1:3000') -> GamerDataService:
    return HTTPGamerDataService(data_service_url=data_service_url)
