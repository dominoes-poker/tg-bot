from aiogram import F
from bot.bot import TGBot

from bot.routers.game_router.create_game_router import CreateGameRouter, create_game_maker_router
from bot.routers.router import TGRouter
from bot.services.game_service.game_data_service import GameDataService
from bot.services.gamer_service import GamerDataService


class RootGameRouter(TGRouter):
    def __init__(self) -> None:
        super().__init__(use_builtin_filters=True, name='RootGameRouter')


def create_root_game_router(bot: TGBot,
                            gamer_data_service: GamerDataService,
                            game_data_service: GameDataService) -> RootGameRouter:
    router = RootGameRouter()
    add_gamers_router: CreateGameRouter = create_game_maker_router(bot, gamer_data_service, game_data_service)
    router.include_router(add_gamers_router)
    return router
