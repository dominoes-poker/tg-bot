from aiogram import F

from bot.dispatcher import TGDispatcher
from bot.routers.game_router.create_game_router import CreateGameRouter, create_game_maker_router
from bot.routers.router import TGRouter
from bot.services.game_service.game_data_service import GameDataService
from bot.services.gamer_service import GamerDataService


class RootGameRouter(TGRouter):
    def __init__(self, add_gamers_router: CreateGameRouter) -> None:
        super().__init__(use_builtin_filters=True, name='RootGameRouter')
        self.setup(add_gamers_router=add_gamers_router)

    def setup(self, add_gamers_router: CreateGameRouter) -> None:
        self.include_router(add_gamers_router)


def create_root_game_router(dispatcher: TGDispatcher,
                       gamer_data_service: GamerDataService,
                       game_data_service: GameDataService) -> RootGameRouter:
    add_gamers_router = create_game_maker_router(dispatcher, gamer_data_service, game_data_service)
    router = RootGameRouter(add_gamers_router)
    router.parent_router = dispatcher
    return router
