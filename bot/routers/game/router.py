from bot.bot import TGBot
from bot.routers.game.create_game import create_start_game_router
from bot.routers.game.round import create_round_router
from bot.routers.router import TGRouter
from bot.services.game_service import GameDataService
from bot.services.player_service import PlayerDataService


def create_root_game_router(bot: TGBot,
                            player_data_service: PlayerDataService,
                            game_data_service: GameDataService) -> TGRouter:
    router = TGRouter(name='<Game> - Router')

    add_gamers_router = create_start_game_router(bot, player_data_service, game_data_service)
    router.include_router(add_gamers_router)

    round_router = create_round_router(bot, game_data_service)
    router.include_router(round_router)

    return router
