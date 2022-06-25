from bot.bot import TGBot
from bot.routers.wellocme.handler import WellcomeHandler
from bot.routers.router import TGRouter
from bot.services.player_service import PlayerDataService


def setup_router(router: TGRouter, handler: WellcomeHandler) -> None:
    router.setup_handler(handler.handle_enter, commands=['start'])

def create_wellcome_router(bot:TGBot,
                           player_data_service: PlayerDataService) -> TGRouter:
    handler = WellcomeHandler(bot, player_data_service)

    router = TGRouter(name='<Wellcome> - Router')
    setup_router(router, handler)

    return router
