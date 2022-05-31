from bot.services.http_gamer_data_service import HTTPGamerDataService


def get_gamer_data_service(data_service_url: str = 'http://127.0.0.1:3000'):
    return HTTPGamerDataService(data_service_url=data_service_url)
