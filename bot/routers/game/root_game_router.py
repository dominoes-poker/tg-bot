from aiogram import F
from bot.bot import TGBot

from bot.routers.game.create_game_router import CreateGameRouter, create_game_maker_router
from bot.routers.game.round_router import create_rpund_router
from bot.routers.router import TGRouter
from bot.services.game_service.game_data_service import GameDataService
from bot.services.player_service import PlayerDataService


class RootGameRouter(TGRouter):
    def __init__(self) -> None:
        super().__init__(use_builtin_filters=True, name='RootGameRouter')


def create_root_game_router(bot: TGBot,
                            player_data_service: PlayerDataService,
                            game_data_service: GameDataService) -> RootGameRouter:
    router = RootGameRouter()
    add_gamers_router: CreateGameRouter = create_game_maker_router(bot, player_data_service, game_data_service)
    router.include_router(add_gamers_router)
    round_router = create_rpund_router(bot, player_data_service, game_data_service)
    router.include_router(round_router)
    return router
