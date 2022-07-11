from bot.bot import DPBot
from bot.routers.wellocme.handler import WellcomeHandler
from bot.routers.router import DPRouter
from services.player_service import PlayerDataService


def setup_router(router: DPRouter, handler: WellcomeHandler) -> None:
    router.setup_handler(handler.handle_enter, commands=['start'])


def create_wellcome_router(bot: DPBot,
                           player_data_service: PlayerDataService) -> DPRouter:
    handler = WellcomeHandler(bot, player_data_service)

    router = DPRouter(name='<Wellcome> - Router')
    setup_router(router, handler)

    return router
