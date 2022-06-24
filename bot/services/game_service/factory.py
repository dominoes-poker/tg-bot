from bot.services.game_service.http_game_data_service import HTTPGameDataService
from bot.services.game_service.game_data_service import GameDataService
from bot.services.loaders import GameLoader, PlayerLoader, RoundLoader
from bot.services.loaders.stake_loader import StakeLoader


def get_game_data_service(data_service_url: str) -> GameDataService:
    round_loader = RoundLoader(StakeLoader())
    game_loader = GameLoader(player_loader=PlayerLoader(), round_loader=round_loader)
    return HTTPGameDataService(data_service_url=data_service_url, loader=game_loader)
