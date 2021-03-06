from bot.bot import DPBot
from bot.routers.game.finish import create_finish_game_router
from bot.routers.game.start import create_start_game_router
from bot.routers.game.round import create_round_router
from bot.routers.router import DPRouter
from services.game_service import GameDataService
from services.player_service import PlayerDataService


def create_root_game_router(bot: DPBot,
                            player_data_service: PlayerDataService,
                            game_data_service: GameDataService) -> DPRouter:
    router = DPRouter(name='<Game> - Router')

    start_game_router = create_start_game_router(bot, player_data_service, game_data_service)
    router.include_router(start_game_router)

    round_router = create_round_router(bot, game_data_service)
    router.include_router(round_router)

    finish_game_router = create_finish_game_router(bot, game_data_service)
    router.include_router(finish_game_router)
    return router
